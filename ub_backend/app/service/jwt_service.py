from uuid import UUID
import jwt

from ub_backend.app.exception.common import UnauthorizedException
from ub_backend.app.exception.jwt import JWTPrefixErrorException
from ub_backend.app.model.token import AccessToken, BaseToken, RefreshToken
from ub_backend.core.config import app_config


class JwtService:
    def __init__(self, secret: UUID, algorithm: str = "HS256"):
        self._secret: str = str(secret)
        self._algorithm: str = algorithm

    def _decode(self, token_str: str) -> dict:
        try:
            return jwt.decode(
                token_str, str(self._secret), algorithms=[self._algorithm]
            )
        except Exception:
            raise UnauthorizedException(
                detail="Invalid auth token", error=("invalid_token")
            )

    def pars_token(self, authorization):
        prefix, _, token_str = authorization.partition(" ")
        if prefix != 'Bearer':
            raise JWTPrefixErrorException()
        return token_str

    def decode_access_token(self, token_str) -> AccessToken:
        data = self._decode(self.pars_token(token_str))
        return AccessToken(**data)

    def decode_refresh_token(self, token_str) -> RefreshToken:
        data = self._decode(token_str)
        if data is None:
            raise UnauthorizedException(
                detail=("Invalid auth token"), error=("invalid_token")
            )
        return RefreshToken(**data) if data else data

    def _encode(self, data: dict) -> bytes:
        return jwt.encode(data, str(self._secret), algorithm=self._algorithm)

    def encode_token(self, token: BaseToken) -> bytes:
        return self._encode(token.dict())


jwt_service = JwtService(secret=app_config.jwt.secret)