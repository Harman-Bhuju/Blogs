from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Re-exports Base so files like main.py can do:
#   from core.database import Base, engine
# to create all database tables in one clean place without having
# to import from both common.models.base and core.database.
from common.models.base import Base
from core.configuration.config import settings

# Read the database URL from application settings.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy Engine.
# The engine is a long-lived object that manages:
#   1. The connection pool (reusable connections to Postgres)
#   2. The SQL dialect (translating Python SQL to PostgreSQL syntax)
#
# Connection Pool parameters:
#   - pool_size: Number of persistent connections kept open in the pool (default is 5).
#   - max_overflow: Extra temporary connections allowed during traffic spikes (default is 10).
#   - pool_timeout: Max seconds to wait for an available connection before raising an error (default is 30).
#   - pool_recycle: Recreates connections after X seconds to prevent stale dropped connections.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Print generated SQL statements in the terminal.
        # --- Connection Pool Settings ---
    pool_size=10,  # 1. Keep up to 10 persistent connections always ready
    max_overflow=20,  # 2. Allow up to 20 temporary extra connections during traffic spikes (Total max = 30)
    pool_timeout=30,  # 3. Wait up to 30 seconds for a connection to free up before throwing a TimeoutError
    pool_recycle=1800,  # 4. Re-create connections after 30 minutes to avoid stale timeouts from PostgreSQL
)



# Provide a database session to FastAPI endpoints.
#
# -> Generator[Session]:
# This is a type hint indicating that get_db is a generator function
# that yields a SQLAlchemy Session object.
#
# What a Session does:
#   • Borrows 1 connection from the Engine's pool.
#   • Tracks changes (e.g. session.add(post)).
#   • Manages transactions (commit() to save or rollback() on error).
#   • Holds the Identity Map (in-memory cache so querying the same
#     post twice in 1 request doesn't hit the DB twice).
#
# Using 'yield' pauses execution and hands the session to FastAPI's route.
# Once the endpoint finishes responding to the client, execution resumes here,
# and exiting the 'with' block automatically closes the session and returns
# the connection back to the engine's pool.
def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session


__all__ = ["Base", "engine", "get_db"]
