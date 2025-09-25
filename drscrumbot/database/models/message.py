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
    orm models related to message domain
"""
from datetime import datetime, timezone

from sqlalchemy import BigInteger, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from drscrumbot.database.models.base import Base


class Message(Base):
    """
        Message model to store telegram chat text message data
    """
    __tablename__: str = "messages"

    id: Mapped[int] = mapped_column(
        # That's because sqlite doesn't incrementing BigInteger
        Integer,
        primary_key=True,
        autoincrement=True
    )

    from_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id")
    )

    # message_id of message is only promised to be unique inside the chat
    chat_message_id: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[datetime] = mapped_column(DateTime)
    # actually telegram message text has limited size, but it's quit large
    # Text is better than String for now
    text: Mapped[str] = mapped_column(Text)
    # message contains other info that should be implemented after mvp phase

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(tz=timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )
