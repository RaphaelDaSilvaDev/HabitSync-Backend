from datetime import datetime

from sqlalchemy.orm import Session

from app.exceptions.api_exception import (
    BadRequestException,
    NotFoundException,
)
from app.main import bcrypt_context
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserOut,
    UserOutFull,
    UserUpdate,
)


class UserService:
    @staticmethod
    def create_user(data: UserCreate, db: Session) -> User:
        existing_user = db.query(User).filter(User.email == data.email).first()

        if existing_user:
            raise BadRequestException('Email already registered')

        password_hash = bcrypt_context.hash(data.password)
        user = User(
            username=data.username,
            email=data.email,
            password=password_hash,
            admin=data.is_admin,
            active=data.is_active,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(id: int, data: UserUpdate, db: Session) -> User:
        existing_user = db.query(User).filter(User.id == id).first()

        if not existing_user:
            raise NotFoundException('User')

        existing_user.username = (
            data.username if data.username else existing_user.username
        )

        if data.password and not data.oldpassword:
            raise BadRequestException('Old password required')
        elif data.password and not bcrypt_context.verify(
            data.oldpassword, existing_user.password
        ):
            raise BadRequestException('Old password not math')

        existing_user.password = (
            bcrypt_context.hash(data.password)
            if data.password
            else existing_user.password
        )
        existing_user.updated_at = datetime.now()

        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    @staticmethod
    def deactivate_user(id: int, db: Session) -> User:
        existing_user = db.query(User).filter(User.id == id).first()

        if not existing_user:
            raise NotFoundException('User')

        if not existing_user.is_active:
            raise BadRequestException('User alreary deactivate')

        existing_user.is_active = False
        existing_user.updated_at = datetime.now()

        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    @staticmethod
    def activate_user(id: int, db: Session) -> User:
        existing_user = db.query(User).filter(User.id == id).first()

        if not existing_user:
            raise NotFoundException('User')

        if existing_user.is_active:
            raise BadRequestException('User alreary activated')

        existing_user.is_active = True
        existing_user.updated_at = datetime.now()

        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    @staticmethod
    def get_user_by_id(user: User, db: Session) -> UserOut:
        existing_user = db.query(User).filter(User.id == user.id).first()

        if not existing_user:
            raise NotFoundException('User')

        formated_user = UserOut(
            id=existing_user.id,
            email=existing_user.email,
            username=existing_user.username,
        )

        return formated_user

    # Administrative Services

    @staticmethod
    def get_all_users(db: Session) -> list[UserOutFull]:
        all_users = db.query(User).all()

        formated_users = [
            UserOutFull(
                id=user.id,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                is_admin=user.is_admin,
            )
            for user in all_users
        ]

        return formated_users
