from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional, Dict, List
import os
from functools import lru_cache
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable loading support."""
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # API settings
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Visa API Agentic Chatbot"
    DEBUG: bool = False

    # Authentication
    API_KEY_NAME: str = "X-API-Key"
    API_KEY: str = os.environ.get("API_KEY", "your-api-key")

    # LLM settings
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20240620"
    CLAUDE_API_KEY: str = os.environ.get("CLAUDE_API_KEY", "")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

    # Vector database settings
    CHROMA_PERSIST_DIRECTORY: str = os.environ.get("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    EMBEDDING_MODEL: str = "text-embedding-3-large"

    # Agent settings
    DEFAULT_AGENT: str = "visa_api_agent"
    ALLOWED_AGENTS: List[str] = ["visa_api_agent", "code_generator", "workflow_creator"]

    # Documentation settings
    DOCS_CHUNK_SIZE: int = 1000
    DOCS_CHUNK_OVERLAP: int = 200
    DOCS_PATH: str = os.environ.get("DOCS_PATH", "./data/visa_api_docs")

    # Session settings
    SESSION_EXPIRY_MINUTES: int = 30
    MAX_SESSION_HISTORY: int = 20

    # Logging
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    # In config.py, add these settings
    USE_DATABASE: bool = os.environ.get("USE_DATABASE", "True").lower() in ("true", "1", "yes")
    DB_URL: str = os.environ.get("DB_URL", "sqlite+aiosqlite:///./data/sessions.db")
    ADMIN_BOOTSTRAP_SECRET: str = Field("visa_api_dev_3f29a8c7b6d5e4f3", validation_alias="ADMIN_BOOTSTRAP_SECRET")


@lru_cache()
def get_settings() -> Settings:
    """Create cached settings instance."""
    return Settings()
