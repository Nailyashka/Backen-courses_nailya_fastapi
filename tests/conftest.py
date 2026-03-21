# ruff: noqa: E402
import json
from unittest import mock
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# --- mock кэш ---
def empty_cache(*args, **kwargs):
    def wrapper(func):
        return func
    return wrapper

# Подмена кэша: выключаем кэш во всех тестах
@pytest.fixture(autouse=True)
def patch_cache():
    with mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f):
        yield

# --- импорт проекта ---
from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa: F403
from src.utils.db_manager import DBManager

# --- проверка режима ---
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

# --- фикстуры БД ---
@pytest_asyncio.fixture(scope="function")
async def db():
    """Асинхронная сессия БД для тестов"""
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        try:
            yield db
        finally:
            # Явное закрытие сессии
            await db.session.close()

# --- одноразовая настройка БД для всей сессии ---
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Создание структуры и загрузка тестовых данных"""
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

    yield

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- фикстуры для HTTP клиента ---
@pytest_asyncio.fixture(scope="session")
async def ac():
    """Асинхронный клиент для всех тестов"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(scope="session")
async def authenticated_ac(ac, setup_database):
    """Фикстура для зарегистрированного пользователя"""
    # Регистрируем пользователя
    await ac.post(
        "/auth/register", json={"email": "hot@lala.com", "password": "1234"}
    )

    # Логинимся
    response = await ac.post(
        "/auth/login",
        json={"email": "hot@lala.com", "password": "1234"},
    )

    token = response.json().get("access_token")
    print("\n--- LOGIN TOKEN ---", token, "---\n")
    ac.headers.update({"Authorization": f"Bearer {token}"})

    return ac