from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.exceptions.api_exception import APIException
from app.schemas.response import BaseResponse


async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            status="error", message=exc.message, data=None
        ).model_dump(),
    )


async def not_authendicated_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and exc.detail == "Not authenticated":
        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": "Not authenticated", "data": None},
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
