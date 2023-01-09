from fastapi import FastAPI
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest

from ub_backend.core.config import app_config


@pytest.fixture(scope="session", autouse=True)
def test_app() -> FastAPI:
    from ub_backend.main import app as app_

    return app_

@pytest.fixture(scope="session")
async def fx_client(test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=test_app,
        base_url="http://testserver",
        headers={"DBUser-Agent": f"test-app/{app_config.profile.version}"},
    ) as client, LifespanManager(test_app):
        yield client


@pytest.fixture
async def access_token(
    fx_client: AsyncClient, email_mock, generate_email_code_mock, fx_user
):
    TEST_CODE = "1234"
    generate_email_code_mock(TEST_CODE)
    response = await fx_client.post(
        "/api/v1/user/registration/email_confirm",
        json={"email": fx_user.email, "code": TEST_CODE},
    )
    resp_data = response.json()

    yield resp_data["access_token"]
    