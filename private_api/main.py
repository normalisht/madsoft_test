from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from private_api.api.routers import main_router
from private_api.core.config import settings
from private_api.core.s3_client import create_s3_client, s3_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    s3_client['client'] = create_s3_client()
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    lifespan=lifespan,
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=['localhost', '127.0.0.1', 'public_api', 'private_api'],
)

app.include_router(main_router)
