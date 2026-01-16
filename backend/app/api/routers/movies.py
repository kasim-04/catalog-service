from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.crud.movies import list_movies, get_movie
from app.schemas.movie import MovieListResponse, MovieDetails

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=MovieListResponse)
def movies_list(
    q: str | None = Query(default=None, description="Поиск по названию"),
    genre_id: list[int] | None = Query(default=None, description="Фильтр по жанрам"),
    country_id: list[int] | None = Query(default=None, description="Фильтр по странам"),
    person_id: list[int] | None = Query(default=None, description="Фильтр по персонам"),
    year_from: int | None = Query(default=None, ge=1800),
    year_to: int | None = Query(default=None, ge=1800),
    rating_from: float | None = Query(default=None, ge=0, le=10),
    rating_to: float | None = Query(default=None, ge=0, le=10),
    sort: str = Query(default="title", description="title/-title/rating/-rating/year/-year"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = list_movies(
        db=db,
        q=q,
        genre_ids=genre_id,
        country_ids=country_id,
        person_ids=person_id,
        year_from=year_from,
        year_to=year_to,
        rating_from=rating_from,
        rating_to=rating_to,
        sort=sort,
        page=page,
        size=size,
    )
    return {"items": items, "page": page, "size": size, "total": total}


@router.get("/{movie_id}", response_model=MovieDetails)
def movie_details(movie_id: int, db: Session = Depends(get_db)):
    movie = get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
