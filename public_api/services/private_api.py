from fastapi import File, HTTPException
import httpx
from pydantic import ValidationError

from public_api.core.config import settings
from public_api.schemas.private_api import FileURLResponse, UploadFileResponse


async def upload_file(file: File) -> UploadFileResponse:
    async with httpx.AsyncClient() as client:
        files = {'file': (file.filename, file.file, file.content_type)}
        response = await client.post(
            f'{settings.private_api_url}/upload', files=files
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail='Error uploading image')

    try:
        return UploadFileResponse(**response.json())
    except ValidationError:
        raise HTTPException(status_code=500, detail='Server error')


async def remove_file(filename: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f'{settings.private_api_url}/files/{filename}'
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail='Error remove image')

    return True


async def get_file_url(filename: str) -> FileURLResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{settings.private_api_url}/files/{filename}'
        )

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail='Image not found')

    try:
        return FileURLResponse(**response.json())
    except ValidationError:
        raise HTTPException(status_code=500, detail='Server error')
