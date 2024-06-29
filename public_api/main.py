from fastapi import FastAPI

from public_api.api.routers import main_router
from public_api.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(main_router)


# @app.on_event('startup')
# async def startup():
#     pass
