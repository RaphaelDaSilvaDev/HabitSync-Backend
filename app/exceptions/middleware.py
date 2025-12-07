import traceback

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.exceptions.api_exception import APIException
from app.schemas.response import BaseResponse


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except APIException:
            raise
        except Exception as e:
            # Pega a stack trace resumida
            tb = traceback.format_exc()
            # Loga no console (ou em logging)
            print(f"Exception on {request.method} {request.url}: {str(e)}")
            print(tb)
            return JSONResponse(
                status_code=500,
                content=BaseResponse(
                    status="error", message="Internal server error.", data=None
                ).model_dump(),
            )
