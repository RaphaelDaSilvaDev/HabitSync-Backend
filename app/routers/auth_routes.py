from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.authenticate_schema import LoginReturn, LoginUser
from app.schemas.error_schema import ErrorResponse
from app.schemas.response import BaseResponse
from app.schemas.token_schema import RefreshTokenResponse
from app.services.auth_service import AuthService
from app.utils.database import get_db
from app.utils.security import verify_token

authRouter = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(verify_token)]


@authRouter.post(
    '/login',
    response_model=BaseResponse[LoginReturn],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': BaseResponse[LoginReturn]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
    },
)
async def login(data: LoginUser, db: Session):
    response = await AuthService.authenticate_user(data, db)
    return BaseResponse(
        status='success', message='User logged successfully', data=response
    )


@authRouter.get(
    '/refresh-token',
    response_model=BaseResponse[RefreshTokenResponse],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': BaseResponse[RefreshTokenResponse]},
    },
)
async def refresh_token(user: CurrentUser):
    token = AuthService.refresh_token(user)
    return BaseResponse(
        status='success', message='Token generated successfully', data=token
    )
