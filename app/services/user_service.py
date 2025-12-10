from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.api_exception import (
    BadRequestException,
)
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserOutFull,
    UserUpdate,
)
from app.utils.security import bcrypt_context


class UserService:
    @staticmethod
    async def create_user(data: UserCreate, db: Session) -> User:
        get_user = await db.scalar(
            select(User).where(User.email == data.email)
        )

        if get_user:
            raise BadRequestException('Email already registered')

        password_hash = bcrypt_context.hash(data.password)
        user = User(
            username=data.username,
            email=data.email,
            password=password_hash,
            is_admin=data.is_admin,
            is_active=data.is_active,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user(user: User, data: UserUpdate, db: Session) -> User:

        user.username = data.username if data.username else user.username

        if data.password and not data.oldpassword:
            raise BadRequestException('Old password required')
        elif data.password and not bcrypt_context.verify(
            data.oldpassword, user.password
        ):
            raise BadRequestException('Old password not math')

        user.password = (
            bcrypt_context.hash(data.password)
            if data.password
            else user.password
        )
        user.updated_at = datetime.now()

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def deactivate_user(user: User, db: Session) -> User:
        if not user.is_active:
            raise BadRequestException('User alreary deactivate')

        user.is_active = False
        user.updated_at = datetime.now()

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def activate_user(user: User, db: Session) -> User:
        if user.is_active:
            raise BadRequestException('User alreary activated')

        user.is_active = True
        user.updated_at = datetime.now()

        await db.commit()
        await db.refresh(user)
        return user

    # Administrative Services

    @staticmethod
    async def get_all_users(db: Session) -> list[UserOutFull]:
        result = await db.scalars(select(User))
        all_users = result.all()

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
