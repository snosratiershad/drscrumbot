# Copyright (C) 2025  Salar Nosrati-Ershad salar@roverc.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    Provides a connection manager and utilities to access a database session

    Currently uses sqlite to speed up the development and will be replaced by
    PostgreSQL on demand.
"""
import logging

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

logger: logging.Logger = logging.getLogger(__name__)

# no need for filename to be configurable as will be replaced by postgres soon
SQLITE_DB_FILENAME: str = "db.sqlite3"


class SqliteDatabaseConnection:
    """
        Sqlite database connection manager

        uses SQLAlchemy with aiosqlite driver
    """

    def __init__(self,  filename: str) -> None:
        self.connect_string: str = f"sqlite+aiosqlite:///{filename}"
        self.engine: AsyncEngine = create_async_engine(self.connect_string)
        self.async_session: async_sessionmaker = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def close(self) -> None:
        """
            Closes database connection
        """
        await self.engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
            Get database session
        """
        async with self.async_session() as session:
            session: AsyncSession
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# global instance of connection manager
db_connection: SqliteDatabaseConnection = SqliteDatabaseConnection(
    SQLITE_DB_FILENAME
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
        Generator to get database session
    """
    async with db_connection.get_session() as session:
        yield session
