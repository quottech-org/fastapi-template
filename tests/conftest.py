import asyncio
from datetime import datetime
from decimal import Decimal
import json
from os import environ
import random
import string
from typing import Any, Dict, Union
from unittest import mock
from uuid import uuid4

from fastapi import FastAPI
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest
from pytest_asyncio import fixture as async_fixture
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import Session

from ub_backend.core.logger import logger
from ub_backend.app.service.telegram_service import telegram_service
from ub_backend.core.config import app_config
from ub_backend.database.postgres.db import session
from ub_backend.database.postgres.sqlalchemy_models.good import DBGood
from ub_backend.database.postgres.sqlalchemy_models.user import DBUser

@async_fixture
def test_app() -> FastAPI:
    from ub_backend.main import app as app_

    return app_


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
    

@async_fixture(scope="session")
async def fx_db() -> Union[Session, async_scoped_session]:
    db = session()
    try:
        yield db
    finally:
        await db.close()


@async_fixture
async def fx_client(test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=test_app,
        base_url="http://testserver",
        headers={"DBUser-Agent": f"test-app/{app_config.profile.version}"},
    ) as client, LifespanManager(test_app):
        yield client


@pytest.fixture
def random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
    

@pytest.fixture
def fx_user_data(random_string) -> Dict[str, Any]:
    return {
        "password": "test",
        "nick_name": "Guest",
        "first_name": "Guest",
        "last_name": "Guest",
        "description": "test",
        "birthday": str(datetime.now()),
        "email": f"{random_string}@gmail.com",
        "phone_number": "+77777777777",
    }


@async_fixture
async def fx_db_user(fx_client: AsyncClient, fx_user_data: Dict[str, Any]) -> DBUser:
    response = await fx_client.post(
        "/api/v1/user/",
        json=fx_user_data,
    )
    return DBUser(**response.json())


@async_fixture
async def fx_token_pair(
    fx_client: AsyncClient, fx_db_user, fx_user_data
):
    response = await fx_client.post(
        "/api/v1/auth/login/email",
        json={"email": fx_user_data.get("email"), "password": fx_user_data.get("password")},
    )
    resp_data = response.json()

    return resp_data.get("access_token"), resp_data.get("refresh_token")
    

@pytest.fixture
def fx_access_token(fx_token_pair):
    return fx_token_pair[0]


@pytest.fixture
def fx_refresh_token(fx_token_pair):
    return fx_token_pair[1]
    

@pytest.fixture
def fx_good_data():
    return {
        "title": "test_good",
        "description": "test decription",
        "price_usd": "1.0",
        "price_gel": "2.7",
        "price_rub": "26.8",
    }


@async_fixture
async def fx_db_good(fx_client: AsyncClient, fx_good_data):
    response = await fx_client.post(
        f"/api/v1/good/",
        json=fx_good_data,
    )
    return DBGood(**response.json())


@async_fixture
async def fx_db_good_factory(fx_client: AsyncClient):
    async def create_good(client = fx_client, data: Dict = None):
        response = await client.post(
            f"/api/v1/good/",
            json=data,
        )
        return DBGood(**response.json())
    return create_good


@pytest.fixture(scope="session")
def telegram_service_mock():
    with mock.patch.object(telegram_service, "send_message") as mock_:
        x = mock_.call_args
        async def mock_send_message(self, user_id: int, text: str, disable_notification: bool = False):
            logger.info(f"Telegram sent message to {user_id} with text: {text}")
            return True
        yield mock_send_message
