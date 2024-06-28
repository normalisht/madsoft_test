from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.routers import main_router
from core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=['localhost', '127.0.0.1', 'public_api'],
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    pass