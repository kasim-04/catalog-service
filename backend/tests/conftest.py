import os
from collections.abc import Generator

import pytest
from tests.test_data import seed_reference_data
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool, NullPool

from app.core.db import get_db
from app.main import app
from app.models.base import Base


def _make_engine():
    """
    Priority:
      1) TEST_DATABASE_URL env var (удобно для docker compose + Postgres)
      2) SQLite in-memory (быстро, без зависимостей)
    """
    test_db_url = os.getenv("TEST_DATABASE_URL")
    if test_db_url:
        return create_engine(test_db_url, poolclass=NullPool)

    return create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope="session")
def db_engine():
    engine = _make_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(db_engine) -> Generator[Session, None, None]:
    # transaction-per-test + rollback
    connection = db_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(bind=connection, autocommit=False, autoflush=False)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db_session

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides = original_overrides


@pytest.fixture()
def seeded(db_session):
    return seed_reference_data(db_session)
