from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.error_schema import ErrorResponse
from app.schemas.response import BaseResponse
from app.schemas.user_schema import (
    UserCreate,
    UserOut,
    UserOutFull,
    UserUpdate,
)
from app.services.user_service import UserService
from app.utils.database import get_db
from app.utils.security import verify_admin, verify_token

user_router = APIRouter(prefix='/user', tags=['user'])

Session = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(verify_token)]


@user_router.post(
    '/create',
    response_model=BaseResponse[UserOut],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': BaseResponse[UserOut]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def create_user(data: UserCreate, db: Session):
    response = await UserService.create_user(data, db)
    return BaseResponse(
        status='success',
        message='User created successfully',
        data=UserOut.model_validate(response),
    )


@user_router.patch(
    '/update',
    response_model=BaseResponse[UserOut],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[UserOut]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def update_user(data: UserUpdate, db: Session, user: CurrentUser):
    response = await UserService.update_user(user, data, db)
    return BaseResponse(
        status='success',
        message='User updated successfully',
        data=UserOut.model_validate(response),
    )


@user_router.put(
    '/deactivate',
    response_model=BaseResponse[UserOut],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[UserOut]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def deactivate_user(db: Session, user: CurrentUser):
    response = await UserService.deactivate_user(user, db)
    return BaseResponse(
        status='success',
        message='User deactivated successfully',
        data=UserOut.model_validate(response),
    )


@user_router.put(
    '/activate',
    response_model=BaseResponse[UserOut],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[UserOut]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def activate_user(db: Session, user: CurrentUser):
    response = await UserService.activate_user(user, db)
    return BaseResponse(
        status='success',
        message='User activated successfully',
        data=UserOut.model_validate(response),
    )


@user_router.get(
    '/',
    response_model=BaseResponse[UserOut],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[UserOut]},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
)
async def get_user(user: CurrentUser, db: Session):
    return BaseResponse(
        status='success',
        message='User returned successfully',
        data=user,
    )


# Administrative Routes


@user_router.get(
    '/all-users',
    response_model=BaseResponse[list[UserOutFull]],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[list[UserOutFull]]},
    },
    dependencies=[Depends(verify_admin)],
)
async def get_all_users(db: Session):
    response = await UserService.get_all_users(db)
    return BaseResponse(
        status='success',
        message='All users returned successfully',
        data=response,
    )
