from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    access_token: str
