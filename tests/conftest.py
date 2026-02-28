# ruff: noqa: E402
import json
from unittest import mock


def empty_cache(*args, **kwargs):
    def wrapper(func):
        return func

    return wrapper


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio

from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *  # noqa: F403
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


# Измените на pytest_asyncio.fixture для асинхронных фикстур
@pytest_asyncio.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        try:
            yield db
        finally:
            # Явное закрытие сессии
            await db.session.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Одноразовая настройка БД для всех тестов"""
    # Сбрасываем БД
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Загружаем тестовые данные
    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    # Используем отдельную сессию для настройки данных
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

    yield

    # Очистка после всех тестов
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
async def authenticated_user(ac, setup_database):
    """Фикстура для зарегистрированного пользователя"""
    # Сначала регистрируем
    response = await ac.post(
        "/auth/register", json={"email": "hot@lala.com", "password": "1234"}
    )

    # Затем логинимся для получения токена
    response = await ac.post(
        "/auth/login",
        data={"username": "hot@lala.com", "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = response.json().get("access_token")

    # Устанавливаем токен в заголовки клиента
    ac.headers.update({"Authorization": f"Bearer {token}"})

    return ac


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post("/auth/login", json={"email": "hot@lala.com", "password": "1234"})
    assert ac.cookies
    yield ac
