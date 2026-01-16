from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.association_tables import movie_genre, movie_country, movie_person


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    release_year: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, index=True, nullable=True)

    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    countries = relationship("Country", secondary=movie_country, back_populates="movies")
    persons = relationship("Person", secondary=movie_person, back_populates="movies")
