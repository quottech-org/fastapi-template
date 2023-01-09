from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_db_transactions():
    from ub_backend.database.postgres.db import session, set_session_context
    set_session_context(f"test_{uuid4()}")
    async with session() as session_:
        time = (await session_.execute("SELECT * FROM user")).scalars().first()
        print(time)
    assert time is not None
    