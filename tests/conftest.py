# ruff: noqa: E402
import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool

from src.main import app
from src.models import * # noqa
from httpx import AsyncClient, ASGITransport

from src.schemas.facilities import FacilitiesAdd
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", "r", encoding="utf-8") as file_hotels:
            hotels = json.load(file_hotels)

    with open("tests/mock_rooms.json", "r", encoding="utf-8") as file_rooms:
            rooms = json.load(file_rooms)

    with open("tests/mock_facilities.json", "r", encoding="utf-8") as file_facilities:
            facilities = json.load(file_facilities)

    hotels =[HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    facilities = [FacilitiesAdd.model_validate(facility) for facility in facilities]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.facilities.add_bulk(facilities)
        await db_.commit()

@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
            "/auth/register",
        json={"email":
                  "kot@pes.com",
              "password": "1234"
        }
    )


@pytest.fixture(scope="session")
async def authenticated_ac(ac,register_user):
    await ac.post(
            "/auth/login",
        json={"email":
                  "kot@pes.com",
              "password": "1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac