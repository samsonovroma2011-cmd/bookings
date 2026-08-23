import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.dependencies import get_db
from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images

logging.basicConfig(level=logging.INFO)


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()

    if redis_manager.redis is None:
        raise RuntimeError("Redis connection failed")
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield

    await redis_manager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)