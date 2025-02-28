from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_NODES: str = "redis://localhost:7070,redis://localhost:7071"
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    VIRTUAL_NODES: int = 100
    BATCH_INTERVAL_SECONDS: float = 5.0
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
