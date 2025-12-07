from fastapi import status


class APIException(Exception):
    def __init__(self, message: str, status_code: status = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
