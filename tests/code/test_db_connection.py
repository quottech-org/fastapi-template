from typing import Union
from datetime import datetime

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import text
from sqlalchemy.orm import Session
import pytest


@pytest.mark.asyncio
async def test_db_get_time(fx_db: Union[Session, async_scoped_session]):

    time = (await fx_db.execute(text('SELECT * FROM now()'))).scalars().first()
    assert isinstance(time, datetime)
    