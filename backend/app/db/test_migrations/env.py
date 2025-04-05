from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.database import Base
import os
from dotenv import load_dotenv
from app.models.user import User
from app.models.book import Book
from app.models.review import Review

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
config = context.config
config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=TEST_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
