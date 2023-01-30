from httpx import AsyncClient
from http import HTTPStatus
import pytest

from ub_backend.database.postgres.sqlalchemy_models.good import DBGood



@pytest.mark.asyncio
async def test_add_good(fx_client: AsyncClient, fx_good_data):
    response = await fx_client.post(
        f"/api/v1/good/",
        json=fx_good_data,
    )
    assert response.status_code == HTTPStatus.OK.value
    assert len(response.json().get("id")) == 36


@pytest.mark.asyncio
async def test_get_good(fx_client: AsyncClient, fx_db_good: DBGood):
    response = await fx_client.get(
        f"/api/v1/good/{fx_db_good.id}",
    )
    assert response.status_code == HTTPStatus.OK.value

    assert response.json().get("id") == fx_db_good.id


@pytest.mark.asyncio
async def test_edit_good(fx_client: AsyncClient, fx_db_good: DBGood):
    title = "biba-boba"
    response = await fx_client.get(
        f"/api/v1/good/{fx_db_good.id}",
    )
    assert response.status_code == HTTPStatus.OK.value

    assert response.json().get("title") == fx_db_good.title

    response = await fx_client.put(
        f"/api/v1/good/{fx_db_good.id}",
        json={"title": title},
    )
    assert response.status_code == HTTPStatus.OK.value
    assert response.json().get("title") == title

    response = await fx_client.get(
        f"/api/v1/good/{fx_db_good.id}",
    )
    assert response.status_code == HTTPStatus.OK.value

    assert response.json().get("title") == title
    