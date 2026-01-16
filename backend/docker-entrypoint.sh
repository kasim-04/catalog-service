#!/usr/bin/env sh
set -e

# Wait for Postgres to accept connections (simple SELECT 1)
if [ -n "${DATABASE_URL:-}" ]; then
  echo "Waiting for database..."
  python - <<'PY'
import os
import time
from sqlalchemy import create_engine, text

url = os.environ.get("DATABASE_URL")
engine = create_engine(url, pool_pre_ping=True)

last_err = None
for _ in range(60):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database is ready")
        break
    except Exception as e:
        last_err = e
        time.sleep(1)
else:
    print("Database is not ready after 60s")
    raise last_err
PY

  echo "Running migrations..."
  alembic upgrade head

  echo "Seeding data (if empty)..."
  python -m app.seed || true
fi

exec "$@"
