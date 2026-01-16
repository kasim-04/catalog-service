from pydantic import BaseModel
from app.schemas.pagination import PageMeta


class GenreOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GenreListResponse(PageMeta):
    items: list[GenreOut]
