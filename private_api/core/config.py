from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    app_title: str = 'MadSoftTest'
    description: str = 'Test Project'
    secret: str = 'SECRET'
    s3_proxy_url: str = 'http://minio:9000'
    s3_endpoint: str = 'localhost:9000'
    s3_access_key: str = 'access_key'
    s3_secret_key: str = 'secret_key'
    s3_secure: bool = False
    memes_bucket_name: str = 'memes'


settings = Settings()
