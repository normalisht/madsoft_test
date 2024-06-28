from minio import Minio
from datetime import timedelta
from core.config import settings


URL_LIFE_TIME: timedelta = timedelta(hours=1)
URL_LIFE_TIME_WITHOUT_ONE_MINUTE: int = 59


s3_client = Minio(
    settings.s3_endpoint_url,
    settings.s3_access_key,
    settings.s3_secret_key,
    secure=settings.s3_secure,
)

if not s3_client.bucket_exists(settings.memes_bucket_name):
    s3_client.make_bucket(settings.memes_bucket_name)
