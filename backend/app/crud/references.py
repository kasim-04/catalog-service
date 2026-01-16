from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.models.country import Country
from app.models.person import Person


def _paginate(stmt, count_stmt, db: Session, page: int, size: int):
    total = db.execute(count_stmt).scalar_one()
    items = db.execute(stmt.offset((page - 1) * size).limit(size)).scalars().all()
    return items, total


def list_genres(db: Session, search: str | None, page: int, size: int):
    base = select(Genre)
    count = select(func.count(Genre.id))
    if search:
        like = f"%{search.strip()}%"
        base = base.where(Genre.name.ilike(like))
        count = count.where(Genre.name.ilike(like))
    base = base.order_by(Genre.name.asc())
    return _paginate(base, count, db, page, size)


def list_countries(db: Session, search: str | None, page: int, size: int):
    base = select(Country)
    count = select(func.count(Country.id))
    if search:
        like = f"%{search.strip()}%"
        base = base.where(Country.name.ilike(like))
        count = count.where(Country.name.ilike(like))
    base = base.order_by(Country.name.asc())
    return _paginate(base, count, db, page, size)


def list_persons(db: Session, search: str | None, page: int, size: int):
    base = select(Person)
    count = select(func.count(Person.id))
    if search:
        like = f"%{search.strip()}%"
        base = base.where(Person.full_name.ilike(like))
        count = count.where(Person.full_name.ilike(like))
    base = base.order_by(Person.full_name.asc())
    return _paginate(base, count, db, page, size)
