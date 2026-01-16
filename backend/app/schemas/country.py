from pydantic import BaseModel
from app.schemas.pagination import PageMeta


class CountryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CountryListResponse(PageMeta):
    items: list[CountryOut]
