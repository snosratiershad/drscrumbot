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
   handler routing for `/clear` command
"""
import logging

from aiogram import Router, F, types
from aiogram.filters import Command, and_f
from aiogram.exceptions import AiogramError
from sqlalchemy.exc import DatabaseError

from drscrumbot.database import db_connection
from drscrumbot.database.models import Clear
from drscrumbot.utils.messages import CLEAR_MESSAGE

logger: logging.Logger = logging.getLogger(__name__)
router: Router = Router()


@router.message(and_f(Command("clear"), F.from_user))
async def clear_handler(message: types.Message) -> None:
    """
      handler for `/clear` command

      creates a clear record associated with user id to soft-clear
      current session updates, and replies with a message.
    """
    # As from_user is already filtered in router and isn't None
    # The empty from_user is probably because of messages sent in a channel
    assert message.from_user
    try:
        async with db_connection.get_session() as session:
            clear: Clear = Clear(
                user_id=message.from_user.id
            )
            session.add(clear)
            await session.commit()
            await message.reply(CLEAR_MESSAGE)
    except (AiogramError, DatabaseError) as e:
        logger.error(f"Error on generating user update: {e}")
