from starlette import status

from .base import HttpException


class InvalidCredentials(HttpException):
    def __init__(self, message: str = "Invalid credentials."):
        self.message = message
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class UserAlreadyExists(HttpException):
    def __init__(self, message: str = "User already exists."):
        self.message = message
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
