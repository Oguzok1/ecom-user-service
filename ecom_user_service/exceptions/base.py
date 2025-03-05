from starlette.exceptions import HTTPException


class HttpException(HTTPException):
    def __init__(self, status_code, detail: str):
        super().__init__(status_code, detail=detail)
