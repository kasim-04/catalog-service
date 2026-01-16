from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps.admin import require_admin
from app.core.db import get_db
from app.crud.movies import create_movie, update_movie, delete_movie
from app.schemas.movie import MovieDetails, MovieCreate, MovieUpdate


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)


@router.post("/movies", response_model=MovieDetails, status_code=status.HTTP_201_CREATED)
def admin_create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    try:
        movie = create_movie(
            db,
            title=payload.title,
            description=payload.description,
            release_year=payload.release_year,
            rating=payload.rating,
            genre_ids=payload.genre_ids,
            country_ids=payload.country_ids,
            person_ids=payload.person_ids,
        )
        return movie
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/movies/{movie_id}", response_model=MovieDetails)
def admin_update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    try:
        movie = update_movie(
            db,
            movie_id,
            title=payload.title,
            description=payload.description,
            release_year=payload.release_year,
            rating=payload.rating,
            genre_ids=payload.genre_ids,
            country_ids=payload.country_ids,
            person_ids=payload.person_ids,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_movie(movie_id: int, db: Session = Depends(get_db)):
    ok = delete_movie(db, movie_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None
