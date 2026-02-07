import uvicorn
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from arq import create_pool
from arq.connections import RedisSettings
from app.api.v1.addresses import router as address_router
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base

from app.models.address import Address

logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    logger.info("Connecting to database...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    
    app.state.redis_pool = redis_pool
    yield

    logger.info("Closing Redis pool.")
    await redis_pool.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)


app.include_router(address_router, prefix="/api/v1/addresses", tags=["Addresses"])

@app.get("/")
async def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "documentation": "/docs"
    }

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)