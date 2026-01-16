from pydantic import BaseModel, Field


class PageMeta(BaseModel):
    page: int = Field(ge=1, default=1)
    size: int = Field(ge=1, le=100, default=20)
    total: int = Field(ge=0, default=0)
