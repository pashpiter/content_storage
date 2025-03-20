from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR: Path = Path(__file__).parent.parent

STATIC: str = "static"
STATIC_DIR: Path = BASE_DIR / STATIC

FILES: str = 'files'
FILES_DIR: Path = STATIC_DIR / FILES


class AppSettings(BaseSettings):
    def __init__(self):
        STATIC_DIR.mkdir(exist_ok=True)
        FILES_DIR.mkdir(exist_ok=True)
        super().__init__()

    debug: bool = Field('True', alias='DEBUG')
    secret_key: str = Field('secret-key', alias='SECRET_KEY')
    algorithm: str = Field('HS256', alias='ALGORITHM')
    access_token_expire_minutes: int = Field(30, alias='TOKEN_EXPIRE_MINUTES')
    admin_email: str = Field('admin@admin.com', alias='ADMIN_EMAIL')
    admin_password: str = Field('admin', alias='ADMIN_PASSWORD')


class RedisSettings(BaseSettings):
    host: str = Field('localhost', alias='REDIS_HOST')
    port: int = Field(6379, alias='REDIS_PORT')
    num_db: int = Field(0, alias='REDIS_NUM_DB')

    @property
    def redis_url(self) -> str:
        return 'redis://{}:{}/{}'.format(
            self.host,
            self.port,
            self.num_db
        )


class PostgresSettings(BaseSettings):
    host: str = Field('localhost', alias='POSTGRES_HOST')
    port: int = Field(5432, alias='POSTGRES_PORT')
    user: str = Field('postgres', alias='POSTGRES_USER')
    password: str = Field('postgres', alias='POSTGRES_PASSWORD')
    db_name: str = Field('postgres', alias='POSTGRES_DB')

    @property
    def postgres_url(self) -> str:
        return 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db_name
        )


class Settings:
    app: AppSettings = AppSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
