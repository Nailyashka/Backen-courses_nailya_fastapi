from contextlib import asynccontextmanager
from fastapi import Body, FastAPI, Query
import uvicorn


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facility
from src.api.images import router as router_images

# НЕЛЬЗЯ ИЗ ФАЙЛА main.py ИМПОРТИРОВАТЬ ЧТО-ТО  ВДРУГИЕ ФАЙЛЫ!!!!!!!!!!!!!!!!!


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    app.include_router(router_auth)
    app.include_router(router_rooms)
    app.include_router(router_hotels)
    app.include_router(router_facility)
    app.include_router(router_bookings)
    app.include_router(router_images)
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
