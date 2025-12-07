from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginReturn(BaseModel):
    acess_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}
