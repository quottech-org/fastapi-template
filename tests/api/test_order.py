from decimal import Decimal
from uuid import uuid4
from httpx import AsyncClient
from http import HTTPStatus

import pytest
from ub_backend.database.postgres.sqlalchemy_models.good import DBGood
from ub_backend.core.logger import logger
from ub_backend.database.postgres.sqlalchemy_models.user import DBUser


@pytest.mark.asyncio
async def test_create_order(fx_client: AsyncClient, fx_access_token, fx_db_user: DBUser, fx_db_good_factory):
    goods = [
        {
            "title": "CAUCASIAN [DALI]",
            "description": "test decription",
            "price_usd": "1.2",
            "price_gel": "2.7",
            "price_rub": "26.8",
        },
        {
            "title": "Barney's Farm [LSD]",
            "description": "test decription",
            "price_usd": "0.9",
            "price_gel": "2.7",
            "price_rub": "26.8",
        },
        {
            "title": "Box 60x60x160",
            "description": "test decription",
            "price_usd": "220.0",
            "price_gel": "2.7",
            "price_rub": "26.8",
        },
    ]
    cart = [await fx_db_good_factory(data=good) for good in goods]
    response = await fx_client.post(
        f"/api/v1/order/",
        json={
            "order": {
                "client_id": str(fx_db_user.id),
                "type": "selftake",
            },
            "cart": [good.id for good in cart]
        },
        headers={"Authorization": f"Bearer {fx_access_token}"}
    )
    assert response.status_code == HTTPStatus.OK.value
    data = response.json()
    logger.info(data)

    assert len(data.get("goods")) == len(goods)
    
    total_price_count = Decimal("0")
    for good in cart:
        total_price_count += Decimal(good.price_usd)

    assert round(Decimal(data.get("total_price_usd")), 3) == round(total_price_count, 3)
