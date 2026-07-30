from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "ULTRON"

    VERSION: str = "1.0.0"

    DATABASE_URL: str = "sqlite:///./ultron.db"

    GROQ_API_KEY: str

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    REDIS_URL: str = "redis://localhost:6379"

    SECRET_KEY: str = "ultron-development-secret"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()