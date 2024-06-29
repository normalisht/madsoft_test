from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from minio import Minio, S3Error

from private_api.core.config import settings
from private_api.core.constants import (
    URL_LIFE_TIME,
    URL_LIFE_TIME_WITHOUT_ONE_MINUTE,
)
from private_api.core.s3_client import get_s3_client

router = APIRouter()


@router.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    s3_client: Minio = Depends(get_s3_client),
):
    try:
        filename = f'{uuid4().hex}.{file.filename.split(".")[-1]}'
        s3_client.put_object(
            settings.memes_bucket_name, filename, file.file, length=file.size
        )
        return {'filename': filename}
    except S3Error as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get('/files/{filename}')
async def get_file_presigned_url(
    filename: str,
    s3_client: Minio = Depends(get_s3_client),
):
    try:
        s3_client.stat_object(settings.memes_bucket_name, filename)
    except S3Error as e:
        if e.code == 'NoSuchKey':
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
    try:
        presigned_url = s3_client.presigned_get_object(
            settings.memes_bucket_name, filename, expires=URL_LIFE_TIME
        )
        return {
            'url': presigned_url,
            'life_time': URL_LIFE_TIME_WITHOUT_ONE_MINUTE,
            'filename': filename,
        }
    except S3Error as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete('/files/{filename}')
async def remove_file(
    filename: str,
    s3_client: Minio = Depends(get_s3_client),
):
    try:
        s3_client.remove_object(settings.memes_bucket_name, filename)
        return {'result': True}
    except S3Error as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
