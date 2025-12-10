from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.api_exception import BadRequestException
from app.main import bcrypt_context
from app.models.user import User
from app.schemas.authenticate_schema import LoginReturn, LoginUser
from app.schemas.token_schema import RefreshTokenResponse
from app.utils.auth_login import AuthLogin


class AuthService:
    @staticmethod
    async def authenticate_user(data: LoginUser, db: Session) -> LoginReturn:
        user = await db.scalar(select(User).where(User.email == data.email))

        if not user:
            raise BadRequestException('Invalid email or password')
        elif not bcrypt_context.verify(data.password, user.password):
            raise BadRequestException('Invalid email or password')

        access_token = AuthLogin.generate_token(user.id)
        refresh_token = AuthLogin.generate_token(user.id, timedelta(days=7))

        userLogged = LoginReturn(
            access_token=access_token, refresh_token=refresh_token
        )

        return userLogged

    @staticmethod
    def refresh_token(user: User) -> RefreshTokenResponse:
        access_token = AuthLogin.generate_token(user.id)

        token = RefreshTokenResponse(access_token=access_token)

        return token
