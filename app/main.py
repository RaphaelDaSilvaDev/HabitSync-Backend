import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.exceptions.api_exception import APIException
from app.exceptions.handlers import api_exception_handler, not_authendicated_handler
from app.exceptions.middleware import GlobalExceptionMiddleware

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(HTTPException, not_authendicated_handler)
app.add_middleware(GlobalExceptionMiddleware)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

from app.routers.auth_routes import authRouter
from app.routers.habit_routes import habit_router
from app.routers.user_routes import user_router

app.include_router(user_router)
app.include_router(authRouter)
app.include_router(habit_router)
