from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: Optional[str] = None
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
