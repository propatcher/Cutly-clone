import pytest
from httpx import AsyncClient

async def test_get_your_click(auth_ac: AsyncClient,ac: AsyncClient):
    auth_response = await auth_ac.get('/click')
    response = await ac.get("/click")
    assert auth_response.status_code == 200
    assert response.status_code == 401
    