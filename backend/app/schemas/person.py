from pydantic import BaseModel
from app.schemas.pagination import PageMeta


class PersonOut(BaseModel):
    id: int
    full_name: str

    class Config:
        from_attributes = True


class PersonListResponse(PageMeta):
    items: list[PersonOut]
