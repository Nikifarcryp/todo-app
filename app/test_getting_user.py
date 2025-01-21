import pytest
from typing import List
from schemas import TaskSchema
from httpx import ASGITransport, AsyncClient
from main import app as my_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import ASYNC_SQLALCHEMY_DATABASE_URL


@pytest.mark.asyncio
async def test_getting_one_task():
    async with AsyncClient(
            transport=ASGITransport(app=my_app), base_url="http://127.0.0.1:8000/"
    ) as ac:
        response = await ac.get('/todos/get_task/2')
    assert response.status_code == 200
    assert response.json() == {
        "title": "Gift",
        "description": "Gift for mum",
        "id": 2,
        "completed": True
    }


@pytest.mark.asyncio
async def test_getting_many_tasks():
    async with AsyncClient(
            transport=ASGITransport(app=my_app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get('/todos/get_tasks/')
    print(response.status_code)
    assert response.status_code == 200
    assert response.json() == List[TaskSchema]

