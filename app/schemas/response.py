from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StatusEnum(str, Enum):
    success = "success"
    error = "error"


class BaseResponse(BaseModel, Generic[T]):
    status: StatusEnum
    message: str
    data: Optional[T] = None
