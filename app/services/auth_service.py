from datetime import timedelta

from sqlalchemy.orm import Session

from app.exceptions.api_exception import APIException
from app.main import bcrypt_context
from app.models.user import User
from app.schemas.authenticate_schema import LoginReturn, LoginUser
from app.utils.auth_login import AuthLogin


class AuthService:
    @staticmethod
    def authenticate_user(data: LoginUser, db: Session) -> LoginReturn:
        user = db.query(User).filter(User.email == data.email).first()

        if not user:
            raise APIException(message="Invalid email or password", status_code=400)
        elif not bcrypt_context.verify(data.password, user.password):
            raise APIException(message="Invalid email or password", status_code=400)

        access_token = AuthLogin.generate_token(user.id)
        refresh_token = AuthLogin.generate_token(user.id, timedelta(days=7))

        userLogged = LoginReturn(acess_token=access_token, refresh_token=refresh_token)

        return userLogged

    @staticmethod
    def refresh_token(user: User) -> dict:
        access_token = AuthLogin.generate_token(user.id)

        return {"access_token": access_token}
