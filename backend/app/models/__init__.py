from .base import Base  # noqa: F401

# импортируем модели, чтобы Alembic видел metadata
from .movie import Movie  # noqa: F401
from .genre import Genre  # noqa: F401
from .country import Country  # noqa: F401
from .person import Person  # noqa: F401
from .association_tables import (  # noqa: F401
    movie_genre,
    movie_country,
    movie_person,
)
