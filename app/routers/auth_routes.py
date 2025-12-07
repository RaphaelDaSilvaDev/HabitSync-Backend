from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.authenticate_schema import LoginReturn, LoginUser
from app.schemas.response import BaseResponse
from app.services.auth_service import AuthService
from app.utils.auth_login import verify_token
from app.utils.database import get_db

authRouter = APIRouter(prefix="/auth", tags=["auth"])


@authRouter.post("/login", response_model=BaseResponse[LoginReturn])
async def login(data: LoginUser, db: Session = Depends(get_db)):
    user_logged = AuthService.authenticate_user(data, db)
    return BaseResponse(
        status="success", message="User logged successfully", data=user_logged
    )


@authRouter.get("/refresh-token", response_model=BaseResponse[dict])
async def refresh_token(user: User = Depends(verify_token)):
    token = AuthService.refresh_token(user)
    return BaseResponse(
        status="success", message="Token generated successfully", data=token
    )
