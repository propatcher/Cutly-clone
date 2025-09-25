import json
import pytest
import asyncio
from sqlalchemy import insert
from app.settings import settings
from app.database import Base,async_session,engine
from datetime import datetime

from app.users.models import User
from app.clicks.models import Click
from app.links.models import Link

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from app.main import app as FastAPI_app

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    def open_json(model: str):
        with open(f"app/tests/test_{model}.json", "r", encoding='utf-8') as file:
            data = json.load(file)
        
        for item in data:
            if 'created_at' in item:
                date_str = item['created_at'].replace('Z', '')
                item['created_at'] = datetime.fromisoformat(date_str)
            if 'clicked_at' in item:
                date_str = item['clicked_at'].replace('Z', '')
                item['clicked_at'] = datetime.fromisoformat(date_str)
        return data
        
    users = open_json("users")
    clicks = open_json("clicks")
    links = open_json("links")
    
    async with async_session() as session:
        await session.execute(insert(User).values(users))
        await session.execute(insert(Link).values(links))
        await session.execute(insert(Click).values(clicks))
        
        await session.commit()
        
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    
@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=FastAPI_app), base_url="http://test"
    ) as ac:
        yield ac
        
@pytest.fixture(scope="function")
async def auth_ac():
    async with AsyncClient(
        transport=ASGITransport(app=FastAPI_app), base_url="http://test"
    ) as ac:
        login_response = await ac.post("/auth/login", json={
            "email": "ivan.petrov@example.com",
            "password": "secret",
        })
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"

        assert "cutly_access_token" in ac.cookies, "Auth cookie not set!"
        assert ac.cookies["cutly_access_token"]

        yield ac
        
@pytest.fixture(scope='function')
async def session():
    async with async_session() as session:
        yield session
        
