# ruff: noqa
import json
from typing import AsyncGenerator, Any
from unittest import mock
from aiofiles import open


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import * # noqa
from httpx import ASGITransport, AsyncClient
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomTest
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="module")
async def db_module() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


async def load_json_data(filename: str):
    async with open(filename, "r", encoding="utf-8") as json_data:
        json_read = await json_data.read()
        return json.loads(json_read)


@pytest.fixture(scope="session", autouse=True)
async def insert_into_test_data(setup_database):
    hotels_data = await load_json_data("tests/mock_hotels.json")
    rooms_data = await load_json_data("tests/mock_rooms.json")

    hotels_models = [HotelAdd(**hotel) for hotel in hotels_data]
    rooms_models = [RoomTest(**room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_models)
        await db_.rooms.add_bulk(rooms_models)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, insert_into_test_data):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )

@pytest.fixture(scope="session")
async def auth_ac(ac, register_user):
    response = await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )
    assert response.status_code == 200

    assert ac.cookies["access_token"]
    yield ac