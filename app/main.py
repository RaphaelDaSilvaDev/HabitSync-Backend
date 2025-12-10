from fastapi import FastAPI, HTTPException

from app.exceptions.api_exception import APIException
from app.exceptions.handlers import (
    api_exception_handler,
    not_authendicated_handler,
)
from app.exceptions.middleware import GlobalExceptionMiddleware

app = FastAPI()

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(HTTPException, not_authendicated_handler)
app.add_middleware(GlobalExceptionMiddleware)


from app.routers.auth_routes import authRouter  # noqa: E402
from app.routers.habit_routes import habit_router  # noqa: E402
from app.routers.user_routes import user_router  # noqa: E402

app.include_router(user_router)
app.include_router(authRouter)
app.include_router(habit_router)
