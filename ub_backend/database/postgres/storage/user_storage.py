from typing import Union

from pydantic import EmailStr
from ub_backend.app.exception.common import UnauthorizedException

from ub_backend.core.security import verify_password

from . import PGStorage, db_connection, ModelT
from ub_backend.database.postgres.sqlalchemy_models.user import DBUser

class PGUserStorage(PGStorage):

    def __init__(self, db: db_connection):
        super().__init__(db, DBUser)

    async def get_by_email(self, email: EmailStr) -> DBUser:
        return await self.get_one({"email": email})

    async def get_by_email_and_password(self, email: str, password: str) -> DBUser:
        user = await self.get_by_email(email)
        if not user or not verify_password(
            f"{user.salt}{password}", user.hashed_password
        ):
            raise UnauthorizedException(detail="Wrong email or password")
        return user
