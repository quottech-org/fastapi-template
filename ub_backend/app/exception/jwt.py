from http import HTTPStatus

from ub_backend.core.base.htth_exception import BaseHTTPException
    

class JWTPrefixErrorException(BaseHTTPException):
    http_status_enum = HTTPStatus.BAD_REQUEST

    def __init__(self, detail="Wrong JWT prefix is set. 'Bearer' is neccessary", error=None):
        super().__init__(detail, error)
