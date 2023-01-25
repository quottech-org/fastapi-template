from uuid import UUID, uuid4
from httpx import AsyncClient
from http import HTTPStatus
import pytest
from ub_backend.api.depends import access_token

from ub_backend.database.postgres.sqlalchemy_models.user import DBUser


@pytest.mark.asyncio
async def test_get_token(fx_client: AsyncClient, fx_user_data, fx_db_user):
    response = await fx_client.post(
        f"/api/v1/auth/login/email",
        json={
            "email": fx_user_data.get("email"),
            "password": fx_user_data.get("password"),
        }
    )
    assert response.status_code == HTTPStatus.OK.value

    data = response.json()
    assert data.get("access_token") and data.get("refresh_token") is not None
    


@pytest.mark.asyncio
async def test_decode_token(fx_client: AsyncClient, fx_access_token):
    assert len((await access_token(authorization=f"Bearer {fx_access_token}")).user_id) == 36


@pytest.mark.asyncio
async def test_refresh_token(fx_client: AsyncClient, fx_refresh_token):
    response = await fx_client.post(
        f"/api/v1/auth/refresh",
        json={
            "token": fx_refresh_token
        }
    )
    assert response.status_code == HTTPStatus.OK.value

    data = response.json()
    _access_token =  data.get("access_token")
    assert len((await access_token(authorization=f"Bearer {_access_token}")).user_id) == 36