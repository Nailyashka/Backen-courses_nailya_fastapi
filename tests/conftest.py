from httpx import AsyncClient
import pytest

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session",autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"



@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        

@pytest.fixture(scope="session", autouse=True)
async def register_user():
    async with AsyncClient(app=app,base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json = {
                "email":"hot@lala.com",
                "password": "1234"
            }
        )