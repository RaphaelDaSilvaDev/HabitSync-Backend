from datetime import datetime, timedelta, timezone

from fastapi.params import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.exceptions.api_exception import APIException
from app.main import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, oauth2_schema
from app.models.user import User
from app.utils.database import get_db


class AuthLogin:
    def generate_token(
        user_id: int,
        duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    ) -> str:
        expiration_date = datetime.now(timezone.utc) + duration

        information_token = {"sub": str(user_id), "exp": expiration_date}

        jwt_token = jwt.encode(information_token, SECRET_KEY, algorithm=ALGORITHM)
        return jwt_token


def verify_token(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise APIException(
                message="Invalid token or user does not exist", status_code=401
            )

        return user
    except jwt.ExpiredSignatureError:
        raise APIException(message="Token has expired", status_code=401)
    except JWTError:
        raise APIException(message="Invalid Token", status_code=401)


def verify_admin(user: User = Depends(verify_token)):
    if not user.is_admin:
        raise APIException(message="You don't have permission to perform this action")
    return user
