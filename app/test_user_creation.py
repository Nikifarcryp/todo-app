import pytest
from httpx import ASGITransport, AsyncClient
from main import app as my_app
from fastapi import status



@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(
            transport=ASGITransport(app=my_app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.post('/todos/create_task',
                                 data={"title": "Test",
                                       "description": "Test description"})
    assert response.status_code == status.HTTP_201_CREATED


