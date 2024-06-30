import datetime as dt

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from pydantic.types import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from public_api.core.constants import FILE_MAX_SIZE
from public_api.core.db import get_async_session
from public_api.core.pagination import PagedResponseSchema, paginate
from public_api.crud import meme_repository
from public_api.models import Meme
from public_api.schemas.memes import MemeCreate, MemeRead, MemeUpdate
from public_api.services.private_api import (
    get_file_url,
    remove_file,
    upload_file,
)

router = APIRouter()


@router.get('', response_model=PagedResponseSchema[MemeRead])
async def get_memes_list(
    page: int = Query(1, gt=0),
    size: int = Query(25, gt=0),
    session: AsyncSession = Depends(get_async_session),
):
    memes = await meme_repository.get_page(page, size, session)
    for index, meme in enumerate(memes):
        memes[index] = await check_and_update_meme_freshness(meme, session)

    total = await meme_repository.get_count(session)
    return paginate(page, size, memes, total, MemeRead)


@router.get(
    '/{meme_id}',
    response_model=MemeRead,
)
async def get_meme(
    meme_id: UUID4, session: AsyncSession = Depends(get_async_session)
):
    meme = await get_meme_or_404(meme_id, session)
    return await check_and_update_meme_freshness(meme, session)


@router.post('', response_model=MemeRead)
async def create_meme(
    image: UploadFile,
    description: str = Form(None),
    session: AsyncSession = Depends(get_async_session),
):
    await validate_file(image)
    upload_file_response = await upload_file(image)
    response = await get_file_url(upload_file_response.filename)
    expires_at = await get_expires_at(response.life_time)
    return await meme_repository.create(
        MemeCreate(
            description=description,
            image_url=response.url,
            filename=response.filename,
            expires_at=expires_at,
        ),
        session,
    )


@router.put('/{meme_id}', response_model=MemeRead)
async def update_meme(
    meme_id: UUID4,
    description: str = Form(None),
    image: UploadFile = File(None),
    session: AsyncSession = Depends(get_async_session),
):
    meme = await get_meme_or_404(meme_id, session)
    update_data = MemeUpdate()

    if description:
        update_data = MemeUpdate(description=description)

    if image:
        await validate_file(image)
        await remove_file(meme.filename)
        response = await upload_file(image)
        response = await get_file_url(response.filename)

        update_data.image_url = response.url
        update_data.filename = response.filename
        update_data.expires_at = await get_expires_at(response.life_time)

    return await meme_repository.update(meme, update_data, session)


@router.delete(
    '/{meme_id}',
    response_model=MemeRead,
)
async def delete_project(
    meme_id: UUID4, session: AsyncSession = Depends(get_async_session)
):
    meme = await get_meme_or_404(meme_id, session)
    await remove_file(meme.filename)
    return await meme_repository.remove(meme, session)


async def check_and_update_meme_freshness(meme: Meme, session: AsyncSession):
    if meme.expires_at < dt.datetime.now():
        response = await get_file_url(meme.filename)
        expires_at = await get_expires_at(response.life_time)
        return await meme_repository.update(
            meme, MemeUpdate(expires_at=expires_at), session
        )
    return meme


async def get_expires_at(life_time: int):
    return dt.datetime.now() + dt.timedelta(minutes=life_time)


async def get_meme_or_404(meme_id: UUID4, session: AsyncSession):
    meme = await meme_repository.get(meme_id, session)
    if not meme:
        raise HTTPException(status_code=404, detail='Meme not found')
    return meme


async def validate_file(file: UploadFile):
    if file.size > FILE_MAX_SIZE:
        raise HTTPException(status_code=400, detail='File is too large')

    content_type = file.content_type
    if content_type not in [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
    ]:
        raise HTTPException(status_code=400, detail='Invalid file type')
