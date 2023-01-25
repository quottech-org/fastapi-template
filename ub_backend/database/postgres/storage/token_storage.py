from typing import Tuple, Union
from uuid import uuid4

from pydantic import EmailStr
from sqlalchemy import select, update
from ub_backend.app.exception.common import UnauthorizedException

from ub_backend.app.model.token import AccessToken, RefreshToken
from ub_backend.database.postgres.sqlalchemy_models.user import DBUser

from . import PGStorage, db_connection, ModelT
from ub_backend.database.postgres.sqlalchemy_models.refresh_token import DBRefreshToken

class PGTokenStorage(PGStorage):

    def __init__(self, db: db_connection):
        super().__init__(db, DBRefreshToken)

    async def refresh_tokens(
        self, token: RefreshToken
    ) -> Tuple[AccessToken, RefreshToken]:

        # TODO: check user baned
        result = await self._db.execute(
            select(self._model_cls).where(self._model_cls.user_id == token.user_id)
        )
        token_db = result.scalars().first()
        if not token_db:
            raise UnauthorizedException(
                detail=("Invalid auth token"), error=("invalid_token")
            )

        new_refresh_token = str(uuid4())

        await self._db.execute(
            update(self._model_cls)
            .where(self._model_cls.user_id == token.user_id)
            .values(token=new_refresh_token)
        )
        await self._db.commit()
        return (
            AccessToken(
                user_id=token.user_id,
                email=token.email,
            ),
            RefreshToken(
                user_id=token.user_id,
                token=new_refresh_token,
                email=token.email,
            ),
        )

    async def gen_new_tokens(
        self, user: DBUser, is_commit=True
    ) -> Tuple[AccessToken, RefreshToken]:

        refresh_token = DBRefreshToken(user_id=user.id)

        refresh_token_db: DBRefreshToken = (
            (
                await self._db.execute(
                    select(self._model_cls).filter(self._model_cls.user_id == user.id)
                )
            )
            .scalars()
            .first()
        )

        if refresh_token_db:
            new_refresh_token = str(uuid4())
            await self.update(refresh_token_db, {"token": new_refresh_token})
            refresh_token.token = new_refresh_token
        else:
            self._db.add(refresh_token)
            await self._db.flush()
            if is_commit:
                await self._db.commit()
            await self._db.refresh(refresh_token)
            self._db.expunge(refresh_token)

        return (
            AccessToken(
                user_id=str(user.id),
                email=user.email,
            ),
            RefreshToken(
                user_id=str(user.id),
                token=str(refresh_token.token),
                email=user.email,
            ),
        )

