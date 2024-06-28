from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Meme
from schemas.memes import MemeCreate, MemeUpdate


class MemeRepository(CRUDBase[Meme, MemeCreate, MemeUpdate]):
    async def get_page(
        self,
        page: int,
        size: int,
        session: AsyncSession,
    ) -> list[Meme]:
        query = select(self.model).limit(size).offset((page - 1) * size)
        objs = await session.scalars(query)
        return objs.all()


meme_repository = MemeRepository(Meme)
