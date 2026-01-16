from pydantic import BaseModel, Field

from app.schemas.pagination import PageMeta
from app.schemas.genre import GenreOut
from app.schemas.country import CountryOut
from app.schemas.person import PersonOut


class MovieShort(BaseModel):
    id: int
    title: str
    release_year: int | None = None
    rating: float | None = None

    class Config:
        from_attributes = True


class MovieDetails(MovieShort):
    description: str | None = None
    genres: list[GenreOut] = []
    countries: list[CountryOut] = []
    persons: list[PersonOut] = []


class MovieListResponse(PageMeta):
    items: list[MovieShort]


# --- Admin input schemas (добавление/редактирование) ---


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    release_year: int | None = Field(default=None, ge=1800)
    rating: float | None = Field(default=None, ge=0, le=10)

    # Связи задаются по id справочников
    genre_ids: list[int] = Field(default_factory=list)
    country_ids: list[int] = Field(default_factory=list)
    person_ids: list[int] = Field(default_factory=list)


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    release_year: int | None = Field(default=None, ge=1800)
    rating: float | None = Field(default=None, ge=0, le=10)

    # Если поле передано, оно полностью заменяет текущие связи
    genre_ids: list[int] | None = None
    country_ids: list[int] | None = None
    person_ids: list[int] | None = None
