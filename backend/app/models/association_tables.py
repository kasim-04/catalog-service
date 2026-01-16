from sqlalchemy import Table, Column, ForeignKey, Integer, String, UniqueConstraint
from app.models.base import Base

movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("movie_id", "genre_id", name="uq_movie_genre"),
)

movie_country = Table(
    "movie_country",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("country_id", ForeignKey("countries.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("movie_id", "country_id", name="uq_movie_country"),
)

# если позже захочешь роли (actor/director) — уже готово поле role
movie_person = Table(
    "movie_person",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", ForeignKey("persons.id", ondelete="CASCADE"), primary_key=True),
    Column("role", String(50), nullable=True),
    UniqueConstraint("movie_id", "person_id", "role", name="uq_movie_person_role"),
)
