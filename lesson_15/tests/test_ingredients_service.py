import httpx
import pytest
from lesson_15.ingredients_service import app_ingredients

@pytest.fixture
async def ingredients_client():
    async with httpx.AsyncClient(app=app_ingredients, base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_get_ingredients(ingredients_client):
    response = await ingredients_client.get("/ingredients")
    assert response.status_code == 200

    data = response.json()
    assert "flour" in data
    assert "sugar" in data
    assert "yeast" in data
