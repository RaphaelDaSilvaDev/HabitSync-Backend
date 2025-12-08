from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    username: Optional[str] = ''
    password: Optional[str] = ''
    oldpassword: Optional[str] = ''


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {'from_attributes': True}


class UserOutFull(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    is_active: bool

    model_config = {'from_attributes': True}
