import httpx
import pytest
from lesson_15.calculation_service import app_buns

@pytest.fixture
async def test_client():
    async with httpx.AsyncClient(app=app_buns, base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_calculate_buns(test_client):
    response = await test_client.get("/calculate_buns")
    assert response.status_code == 200

    data = response.json()
    assert "buns_possible" in data
