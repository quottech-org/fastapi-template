from http import HTTPStatus

from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    http_status_enum: HTTPStatus = HTTPStatus.BAD_GATEWAY

    def __init__(self, detail=None, error=None):

        self.status_code = self.http_status_enum.value
        self.error = error if error else self.http_status_enum.phrase
        self.detail = detail if detail else self.http_status_enum.description
