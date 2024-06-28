from fastapi import FastAPI

from api.routers import main_router
from core.config import settings
from fastapi_pagination import add_pagination

app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(main_router)

add_pagination(app)


@app.on_event('startup')
async def startup():
    pass
