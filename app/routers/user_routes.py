from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

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
from app.utils.auth_login import verify_admin, verify_token
from app.utils.database import get_db

user_router = APIRouter(prefix='/user', tags=['user'])


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
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    created_user = await UserService.create_user(data, db)
    return BaseResponse(
        status='success',
        message='User created successfully',
        data=UserOut.model_validate(created_user),
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
async def update_user(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(verify_token),
):
    updated_user = await UserService.update_user(user.id, data, db)
    return BaseResponse(
        status='success',
        message='User updated successfully',
        data=UserOut.model_validate(updated_user),
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
async def deactivate_user(
    db: Session = Depends(get_db), user: User = Depends(verify_token)
):
    deactivated_user = await UserService.deactivate_user(user.id, db)
    return BaseResponse(
        status='success',
        message='User deactivated successfully',
        data=UserOut.model_validate(deactivated_user),
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
async def activate_user(
    db: Session = Depends(get_db), user: User = Depends(verify_token)
):
    activated_user = await UserService.activate_user(user.id, db)
    return BaseResponse(
        status='success',
        message='User activated successfully',
        data=UserOut.model_validate(activated_user),
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
async def get_user_by_id(
    user: User = Depends(verify_token), db: Session = Depends(get_db)
):
    user = await UserService.get_user_by_id(user, db)
    return BaseResponse(
        status='success', message='User returned successfully', data=user
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
async def get_all_users(db: Session = Depends(get_db)):
    all_users = await UserService.get_all_users(db)
    return BaseResponse(
        status='success',
        message='All user returned successfully',
        data=all_users,
    )
