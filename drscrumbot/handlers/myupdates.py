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
   handler routing for `/myupdates`
"""
import logging

from aiogram import Router, F, types
from aiogram.filters import Command, and_f
from aiogram.exceptions import AiogramError
from sqlalchemy import select, Result
from sqlalchemy.exc import DatabaseError

from drscrumbot.database import db_connection
from drscrumbot.database.models import Message
from drscrumbot.utils.messages import UPDATE_MESSAGE

logger: logging.Logger = logging.getLogger(__name__)
router: Router = Router()


@router.message(and_f(Command("myupdates"), F.from_user))
async def myupdates_handler(message: types.Message) -> None:
    """
      handler for `/myupdates` command

      replies a list of updates from user messages with time
    """
    # As from_user is already filtered in router and is'nt None
    # The empty from_user is probably because of messages sent in a channel
    assert message.from_user

    try:
        async with db_connection.get_session() as session:
            result: Result = await session.execute(
                select(Message).
                where(Message.from_user_id == message.from_user.id).
                order_by(Message.date)
            )
            updates: str = "\n".join(map(
                lambda row: f"{row[0].date}: {row[0].text}",
                result.all()
            ))
            await message.reply(UPDATE_MESSAGE.format(updates=updates))
    except (AiogramError, DatabaseError) as e:
        logger.error(f"Error on generating user update: {e}")
