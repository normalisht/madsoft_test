from minio import Minio
import urllib3

from private_api.core.config import settings

s3_client: dict[str, Minio] = {'client': None}


def get_s3_client() -> Minio:
    return s3_client['client']


def create_s3_client() -> Minio:
    client = Minio(
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
    if not client.bucket_exists(settings.memes_bucket_name):
        client.make_bucket(settings.memes_bucket_name)
    return client
