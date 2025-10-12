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
    orm models related to update domain
"""
from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    Text,
    ForeignKey,
    Table,
    Column
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from drscrumbot.database.models.base import Base


# it's an association table for many-to-many relationship
update_message: Table = Table(
    "update_message",
    Base.metadata,
    Column("message_id", ForeignKey("messages.id")),
    Column("update_id", ForeignKey("updates.id"))
)


class Update(Base):
    """
        Update model to store user's generated update report
    """
    __tablename__: str = "updates"

    id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            autoincrement=True
        )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id")
    )
    text: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(tz=timezone.utc),
        onupdate=lambda: datetime.now(tz=timezone.utc)
    )

    messages = relationship(
        "Message",
        secondary=update_message,
        back_populates="updates",
    )
