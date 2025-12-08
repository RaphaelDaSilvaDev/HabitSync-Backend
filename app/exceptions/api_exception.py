from fastapi import status


class APIException(Exception):
    def __init__(
        self, message: str, status_code: status = status.HTTP_400_BAD_REQUEST
    ):
        self.status_code = status_code
        self.message = message


class NotFoundException(APIException):
    def __init__(self, item: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, message=f'{item} not found'
        )


class BadRequestException(APIException):
    def __init__(self, message: str = 'Bad request'):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, message=message
        )


class UnauthorizedException(APIException):
    def __init__(
        self,
        message: str = 'You do not have permission to perform this action.',
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message=message
        )


class ForbiddenException(APIException):
    def __init__(self, message: str = 'Not allowed'):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, message=message
        )
