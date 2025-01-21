from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import ASYNC_SQLALCHEMY_DATABASE_URL
import pytest

@pytest.mark.asyncio
async def test_db():
    engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(select(1))
        assert result.scalar() == 1
