import pytest


@pytest.mark.asyncio
async def test_load_test_config():
    from ub_backend.core.config import app_config, EnvirometTypes

    assert app_config.enviroment == EnvirometTypes.dev
    