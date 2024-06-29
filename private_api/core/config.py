from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    app_title: str = 'MadSoftTest'
    description: str = 'Test Project'
    secret: str = 'SECRET'
    memes_bucket_name: str = 'memes'
    s3_endpoint_url: str = 'minio.example.com'
    s3_access_key: str = 'access_key'
    s3_secret_key: str = 'secret_key'
    s3_secure: bool = False


settings = Settings()
