from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'MadSoftTest'
    description: str = 'Test Project'
    secret: str = 'SECRET'
    memes_bucket_name: str = 'memes'
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_secure: bool

    class Config:
        env_file = '.env'


settings = Settings()
