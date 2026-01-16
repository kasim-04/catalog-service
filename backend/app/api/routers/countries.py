from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.crud.references import list_countries
from app.schemas.country import CountryListResponse

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("", response_model=CountryListResponse)
def get_countries(
    search: str | None = Query(default=None, description="Поиск по названию страны"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = list_countries(db, search, page, size)
    return {"items": items, "page": page, "size": size, "total": total}
