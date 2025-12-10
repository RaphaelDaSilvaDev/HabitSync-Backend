from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions.api_exception import (
    BadRequestException,
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
    async def create_user(data: UserCreate, db: Session) -> User:
        existing_user = await db.scalar(
            select(User).where(User.email == data.email)
        )

        if existing_user:
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
    async def update_user(id: int, data: UserUpdate, db: Session) -> User:
        existing_user: User = await db.scalar(
            select(User).where(User.id == id)
        )

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
        await db.commit()
        await db.refresh(existing_user)
        return existing_user

    @staticmethod
    async def deactivate_user(id: int, db: Session) -> User:
        existing_user: User = await db.scalar(
            select(User).where(User.id == id)
        )

        if not existing_user.is_active:
            raise BadRequestException('User alreary deactivate')

        existing_user.is_active = False
        existing_user.updated_at = datetime.now()

        await db.commit()
        await db.refresh(existing_user)
        return existing_user

    @staticmethod
    async def activate_user(id: int, db: Session) -> User:
        existing_user = await db.scalar(select(User).where(User.id == id))

        if existing_user.is_active:
            raise BadRequestException('User alreary activated')

        existing_user.is_active = True
        existing_user.updated_at = datetime.now()

        await db.commit()
        await db.refresh(existing_user)
        return existing_user

    @staticmethod
    async def get_user(user: User, db: Session) -> UserOut:
        existing_user = await db.scalar(select(User).where(User.id == user.id))

        formated_user = UserOut(
            id=existing_user.id,
            email=existing_user.email,
            username=existing_user.username,
        )

        return formated_user

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
