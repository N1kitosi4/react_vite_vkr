from typing import Optional
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    img: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
