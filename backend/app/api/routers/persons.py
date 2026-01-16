from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.crud.references import list_persons
from app.schemas.person import PersonListResponse

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("", response_model=PersonListResponse)
def get_persons(
    search: str | None = Query(default=None, description="Поиск по ФИО персоны"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = list_persons(db, search, page, size)
    return {"items": items, "page": page, "size": size, "total": total}
