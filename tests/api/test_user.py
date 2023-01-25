from uuid import uuid4
from httpx import AsyncClient
from http import HTTPStatus
import pytest

from ub_backend.database.postgres.sqlalchemy_models.user import DBUser


@pytest.mark.asyncio
async def test_get_existed_user(fx_client: AsyncClient, fx_db_user: DBUser):
    response = await fx_client.get(
        f"/api/v1/user/{str(fx_db_user.id)}",
    )
    assert response.status_code == HTTPStatus.OK.value
    assert response.json().get("id") == fx_db_user.id


@pytest.mark.asyncio
async def test_get_not_existed_user(fx_client: AsyncClient):
    response = await fx_client.get(
        f"/api/v1/user/{str(uuid4())}",
    )
    assert response.status_code == HTTPStatus.NOT_FOUND.value
    