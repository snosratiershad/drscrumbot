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
   handler routing for `/start` command
"""
import logging

from aiogram import Router, F, types
from aiogram.filters import CommandStart, and_f
from aiogram.exceptions import AiogramError
from sqlalchemy.exc import IntegrityError

from drscrumbot.database import db_connection
from drscrumbot.database.models import User
from drscrumbot.utils.messages import WELCOME_MESSAGE

logger: logging.Logger = logging.getLogger(__name__)
router: Router = Router()


@router.message(and_f(CommandStart(), F.from_user))
async def start_handler(message: types.Message) -> None:
    """
        handler for `/start` command

        replies a greeting including users full name
    """
    # As from_user is already filtered in router and is'nt None
    # The empty from_user is probably because of messages sent in a channel
    assert message.from_user
    try:
        async with db_connection.get_session() as session:
            user: User = User(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code
            )
            session.add(user)
            await session.commit()
    except IntegrityError:
        # unique constraint failed
        # solution is db-specific so I wait for postgresql
        pass

    user_fullname: str = message.from_user.full_name

    try:
        await message.answer(
            WELCOME_MESSAGE.format(full_name=user_fullname),
            reply_to_message_id=message.message_id
        )
    except AiogramError as e:
        logger.error(f"error in start handler: {e}")
