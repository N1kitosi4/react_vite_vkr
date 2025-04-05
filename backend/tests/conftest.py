import os
import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, get_db

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
ALEMBIC_CONFIG_PATH = "test_alembic.ini"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    alembic_cfg = Config(ALEMBIC_CONFIG_PATH)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

    yield


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
