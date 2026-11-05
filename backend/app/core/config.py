import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "EmpowerMSME Backend"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "super-secret-empower-msme-key-32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    DATABASE_URL: str = "sqlite:///./empower_msme.db"
    GEMINI_API_KEY: str = ""
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def clean_db_url(cls, v: str) -> str:
        if not v or v.startswith("file:"):
            backend_dir = Path(__file__).resolve().parent.parent.parent
            db_path = backend_dir / "empower_msme.db"
            # Normalize for Windows: use forward slashes
            return f"sqlite:///{db_path.as_posix()}"
        return v

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
