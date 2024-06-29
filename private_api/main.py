from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from private_api.api.routers import main_router
from private_api.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=['localhost', '127.0.0.1', 'public_api', 'private_api'],
)

app.include_router(main_router)
