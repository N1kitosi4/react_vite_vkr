import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Book Reviews App"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
