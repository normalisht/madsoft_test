import os

from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
import pytest
from pytest_minio_mock.plugin import MockMinioClient

from private_api.core.s3_client import get_s3_client
from private_api.main import app

load_dotenv()

s3_client = MockMinioClient(
    endpoint=os.getenv('S3_ENDPOINT'),
    access_key=os.getenv('S3_ACCESS_KEY'),
    secret_key=os.getenv('S3_SECRET_KEY'),
    secure=os.getenv('S3_SECURE') == 'True',
)
memes_bucket_name = os.getenv('MEMES_BUCKET_NAME') or 'memes'
if not s3_client.bucket_exists(memes_bucket_name):
    s3_client.make_bucket(memes_bucket_name)


def override_get_s3_client() -> MockMinioClient:
    return s3_client


app.dependency_overrides[get_s3_client] = override_get_s3_client


@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://public_api',
    ) as ac:
        yield ac
