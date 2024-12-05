from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    # Redis
    redis_host: str
    redis_port: int
    redis_password: str

    # JWT
    jwt_secret_key: str
    jwt_expire_time_seconds: int
    jwt_algorithm: str

    # Database
    db_username: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    echo_sql: bool

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
