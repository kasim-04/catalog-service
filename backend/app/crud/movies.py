from app.models.genre import Genre
from app.models.country import Country
from app.models.person import Person

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from app.models.movie import Movie


def _load_reference_entities(
    db: Session,
    *,
    genre_ids: list[int] | None,
    country_ids: list[int] | None,
    person_ids: list[int] | None,
):
    """Загрузка справочников по id.

    Возвращает кортеж (genres, countries, persons). Если какие-то id не найдены,
    кидает ValueError с сообщением для ответа 400.
    """

    genres: list[Genre] = []
    countries: list[Country] = []
    persons: list[Person] = []

    if genre_ids is not None:
        if genre_ids:
            genres = db.execute(select(Genre).where(Genre.id.in_(genre_ids))).scalars().all()
            missing = sorted(set(genre_ids) - {g.id for g in genres})
            if missing:
                raise ValueError(f"Unknown genre_ids: {missing}")

    if country_ids is not None:
        if country_ids:
            countries = db.execute(select(Country).where(Country.id.in_(country_ids))).scalars().all()
            missing = sorted(set(country_ids) - {c.id for c in countries})
            if missing:
                raise ValueError(f"Unknown country_ids: {missing}")

    if person_ids is not None:
        if person_ids:
            persons = db.execute(select(Person).where(Person.id.in_(person_ids))).scalars().all()
            missing = sorted(set(person_ids) - {p.id for p in persons})
            if missing:
                raise ValueError(f"Unknown person_ids: {missing}")

    return genres, countries, persons


def list_movies(
    db: Session,
    q: str | None,
    genre_ids: list[int] | None,
    country_ids: list[int] | None,
    person_ids: list[int] | None,
    year_from: int | None,
    year_to: int | None,
    rating_from: float | None,
    rating_to: float | None,
    sort: str,
    page: int,
    size: int,
):
    stmt = select(Movie)
    # фильтры по связям
    if genre_ids:
        stmt = stmt.where(Movie.genres.any(Genre.id.in_(genre_ids)))
    if country_ids:
        stmt = stmt.where(Movie.countries.any(Country.id.in_(country_ids)))
    if person_ids:
        stmt = stmt.where(Movie.persons.any(Person.id.in_(person_ids)))

    # поиск и числовые фильтры
    if q and q.strip():
        like = f"%{q.strip()}%"
        stmt = stmt.where(Movie.title.ilike(like))
    if year_from is not None:
        stmt = stmt.where(Movie.release_year >= year_from)
    if year_to is not None:
        stmt = stmt.where(Movie.release_year <= year_to)
    if rating_from is not None:
        stmt = stmt.where(Movie.rating >= rating_from)
    if rating_to is not None:
        stmt = stmt.where(Movie.rating <= rating_to)

    # сортировка
    # sort: "title", "-title", "rating", "-rating", "year", "-year"
    order_map = {
        "title": Movie.title.asc(),
        "-title": Movie.title.desc(),
        "rating": Movie.rating.asc(),
        "-rating": Movie.rating.desc(),
        "year": Movie.release_year.asc(),
        "-year": Movie.release_year.desc(),
    }
    stmt = stmt.order_by(order_map.get(sort, Movie.title.asc()))

    # count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    items = (
        db.execute(stmt.offset((page - 1) * size).limit(size))
        .scalars()
        .all()
    )
    return items, total


def get_movie(db: Session, movie_id: int) -> Movie | None:
    stmt = (
        select(Movie)
        .where(Movie.id == movie_id)
        .options(
            selectinload(Movie.genres),
            selectinload(Movie.countries),
            selectinload(Movie.persons),
        )
    )
    return db.execute(stmt).scalar_one_or_none()


def create_movie(
    db: Session,
    *,
    title: str,
    description: str | None,
    release_year: int | None,
    rating: float | None,
    genre_ids: list[int],
    country_ids: list[int],
    person_ids: list[int],
) -> Movie:
    genres, countries, persons = _load_reference_entities(
        db,
        genre_ids=genre_ids,
        country_ids=country_ids,
        person_ids=person_ids,
    )

    movie = Movie(
        title=title,
        description=description,
        release_year=release_year,
        rating=rating,
    )
    movie.genres = genres
    movie.countries = countries
    movie.persons = persons

    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(
    db: Session,
    movie_id: int,
    *,
    title: str | None,
    description: str | None,
    release_year: int | None,
    rating: float | None,
    genre_ids: list[int] | None,
    country_ids: list[int] | None,
    person_ids: list[int] | None,
) -> Movie | None:
    movie = get_movie(db, movie_id)
    if not movie:
        return None

    if title is not None:
        movie.title = title
    if description is not None:
        movie.description = description
    if release_year is not None:
        movie.release_year = release_year
    if rating is not None:
        movie.rating = rating

    # связи заменяем только если поле передано
    if genre_ids is not None or country_ids is not None or person_ids is not None:
        genres, countries, persons = _load_reference_entities(
            db,
            genre_ids=genre_ids,
            country_ids=country_ids,
            person_ids=person_ids,
        )
        if genre_ids is not None:
            movie.genres = genres
        if country_ids is not None:
            movie.countries = countries
        if person_ids is not None:
            movie.persons = persons

    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int) -> bool:
    movie = db.get(Movie, movie_id)
    if not movie:
        return False
    db.delete(movie)
    db.commit()
    return True
