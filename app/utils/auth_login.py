from datetime import datetime, timedelta, timezone

from fastapi.params import Depends
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.api_exception import UnauthorizedException
from app.main import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    oauth2_schema,
)
from app.models.user import User
from app.utils.database import get_db


class AuthLogin:
    def generate_token(
        user_id: int,
        duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    ) -> str:
        expiration_date = datetime.now(timezone.utc) + duration

        information_token = {'sub': str(user_id), 'exp': expiration_date}

        jwt_token = jwt.encode(
            information_token, SECRET_KEY, algorithm=ALGORITHM
        )
        return jwt_token


async def verify_token(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = int(payload.get('sub'))
        user = await db.scalar(select(User).where(User.id == user_id))

        if not user:
            raise UnauthorizedException('Invalid token or user does not exist')

        return user
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException('Token has expired')
    except JWTError:
        raise UnauthorizedException('Invalid Token')


def verify_admin(user: User = Depends(verify_token)):
    if not user.is_admin:
        raise UnauthorizedException()
    return user
