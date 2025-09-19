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
    orm models related to user domain
"""
from datetime import datetime, timezone

from sqlalchemy import BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from drscrumbot.database.models.base import Base


class User(Base):
    """
        User model to store telegram user information
    """
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )
    created_at: Mapped[str | None] = mapped_column(
        DateTime,
        default=datetime.now(tz=timezone.utc)
    )
    updated_at: Mapped[str | None] = mapped_column(
        DateTime,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )
    is_active: Mapped[str | None] = mapped_column(Boolean, default=True)
