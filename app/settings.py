from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    secret_key: str
    env: str
    log_level: str
    backend_host_url: str
    frontend_host_url: str

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
