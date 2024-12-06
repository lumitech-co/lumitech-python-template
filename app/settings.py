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
    db_url: str
    echo_sql: bool


settings = Settings()
