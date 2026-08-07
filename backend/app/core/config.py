from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =====================================================
    # Project
    # =====================================================

    PROJECT_NAME: str = "ULTRON"

    VERSION: str = "1.0.0"

    # =====================================================
    # Database
    # =====================================================

    DATABASE_URL: str = "sqlite:///./ultron.db"

    # =====================================================
    # LLM
    # =====================================================

    GROQ_API_KEY: str

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Future Providers
    OPENAI_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""

    # =====================================================
    # Embeddings
    # =====================================================

    EMBEDDING_PROVIDER: str = "huggingface"

    EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # =====================================================
    # Vector Database
    # =====================================================

    VECTOR_DB: str = "chroma"

    VECTOR_DB_PATH: str = "./vector_db"

    # =====================================================
    # Memory
    # =====================================================

    MEMORY_TOP_K: int = 5

    # =====================================================
    # Redis
    # =====================================================

    REDIS_URL: str = "redis://localhost:6379"

    # =====================================================
    # Authentication
    # =====================================================

    SECRET_KEY: str = "ultron-development-secret"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =====================================================
    # GitHub
    # =====================================================

    GITHUB_USERNAME: str = ""

    GITHUB_TOKEN: str = ""

    # =====================================================
    # Settings
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()