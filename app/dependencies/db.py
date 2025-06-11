# app/dependencies/db.py
from typing import Any, AsyncGenerator
from app.db.session import AsyncSessionLocal

async def get_db() -> AsyncGenerator[Any, Any]:
    async with AsyncSessionLocal() as session:
        yield session
