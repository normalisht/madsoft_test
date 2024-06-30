import urllib3
from minio import Minio

from private_api.core.config import settings

s3_client = Minio(
    settings.s3_endpoint,
    settings.s3_access_key,
    settings.s3_secret_key,
    secure=settings.s3_secure,
    http_client=urllib3.ProxyManager(
        settings.s3_proxy_url,
        timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
        retries=urllib3.Retry(
            total=5,
            backoff_factor=0.2,
            status_forcelist=[500, 502, 503, 504],
        ),
    ),
)

if not s3_client.bucket_exists(settings.memes_bucket_name):
    s3_client.make_bucket(settings.memes_bucket_name)


def get_s3_client() -> Minio:
    return s3_client
