from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.api_exception import APIException
from app.schemas.response import BaseResponse


async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            status='error', message=exc.message, data=None
        ).model_dump(),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = [
        {
            'field': '.'.join(str(loc) for loc in err['loc']),
            'message': err['msg'],
        }
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=BaseResponse(
            status='error', message='Invalid request data', data=errors
        ).model_dump(),
    )
