from minio import Minio

from private_api.core.config import settings

s3_client = Minio(
    settings.s3_endpoint_url,
    settings.s3_access_key,
    settings.s3_secret_key,
    secure=settings.s3_secure,
)

if not s3_client.bucket_exists(settings.memes_bucket_name):
    s3_client.make_bucket(settings.memes_bucket_name)


def get_s3_client() -> Minio:
    return s3_client
