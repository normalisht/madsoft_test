from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    app_title: str = 'MadSoftTest'
    description: str = 'Test Project'
    secret: str = 'SECRET'
    db_driver: str = 'postgresql+asyncpg'
    db_host: str = 'postgres_db'
    db_port: int = '5454'
    db_name: str = 'madsoft_test'
    db_user: str = 'postgres'
    db_password: str = 'postgres'
    private_api_url: str = 'http://private_api:8001'

    @property
    def db_url(self) -> str:
        return (
            f'{settings.db_driver}://{settings.db_user}:{settings.db_password}'
            f'@{settings.db_host}:{settings.db_port}/{settings.db_name}'
        )


settings = Settings()
