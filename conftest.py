import pytest
from httpx import AsyncClient , ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession , async_sessionmaker , create_async_engine

from main import app
from app.database.connection import get_db
from app.models.base import Base

TEST_DATABASE_URL="sqlite+aiosqlite:///./test.db"

test_engine=create_async_engine(TEST_DATABASE_URL)
test_session=async_sessionmaker(test_engine,expire_on_commit=False,class_=AsyncSession)

@pytest.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    async def override_get_db():
        async with test_session() as session:
            yield session
    app.dependency_overrides[get_db]=override_get_db
    async with AsyncClient(transport=ASGITransport(app=app),base_url="https://test") as c:
        yield c
    
    app.dependency_overrides.clear()

@pytest.fixture
async def registered_client(client):
    data={
        "username":"User1",
        "password":"12345"
    }
    await client.post("/auth/register",json=data)
    login=await client.post("/auth/login",data=data)
    res_login=login.json()
    token=res_login["access_token"]
    """token=(login.json())[access_token]"""
    client.headers.update({"Authorization":f"Bearer {token}"})
    return client

@pytest.fixture
async def created_note(registered_client):
    data={
        "head":"test1",
        "content":"this is test"
    }
    note=await registered_client.post("/notes/",json=data)
    return note.json()
    