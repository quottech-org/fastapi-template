from http import HTTPStatus

from ub_backend.core.base.htth_exception import BaseHTTPException



class NotFoundException(BaseHTTPException):
    http_status_enum = HTTPStatus.NOT_FOUND


class BadRequestExcetion(BaseHTTPException):
    http_status_enum = HTTPStatus.BAD_REQUEST
    

class UnauthorizedException(BaseHTTPException):
    http_status_enum = HTTPStatus.UNAUTHORIZED
