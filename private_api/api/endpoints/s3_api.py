from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException
from minio import S3Error

from core.config import settings
from core.s3_client import (
    s3_client,
    URL_LIFE_TIME,
    URL_LIFE_TIME_WITHOUT_ONE_MINUTE,
)

router = APIRouter()


@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
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
async def get_file_presigned_url(filename: str):
    try:
        print(filename)
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
async def remove_file(filename: str):
    try:
        s3_client.remove_object(settings.memes_bucket_name, filename)
        return {'result': True}
    except S3Error as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )
