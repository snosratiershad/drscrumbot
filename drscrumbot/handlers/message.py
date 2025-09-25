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
   handler routing for messages to be recorded
"""
import logging

from aiogram import Router, F, types
from aiogram.exceptions import AiogramError
from sqlalchemy.exc import InvalidRequestError

from drscrumbot.database import db_connection
from drscrumbot.database.models import Message
from drscrumbot.utils.messages import (
    NON_TEXT_MESSAGE_ERROR_MESSAGE,
    MESSAGE_RECORD_FAILED_ERROR_MESSAGE
)

logger: logging.Logger = logging.getLogger(__name__)

router: Router = Router()


@router.message(F.text & ~F.text.startswith("/") & F.from_user)
async def message_handler(message: types.Message) -> None:
    """
        handles regular text messages
    """
    # As from_user is already filtered in router and is'nt None
    # The empty from_user is probably because of messages sent in a channel
    assert message.from_user
    # We should check if the sender message is already exists on db
    # otherwise the error in insert of `/start` command will cause panic
    try:
        async with db_connection.get_session() as session:
            message_record: Message = Message(
                from_user_id=message.from_user.id,
                chat_message_id=message.message_id,
                date=message.date,
                text=message.text
            )
            session.add(message_record)
            await session.commit()
    except InvalidRequestError as e:
        # It's probably is because related user is not exists in db
        logger.error(f"Error when inserting message: {e}")
        await message.reply(MESSAGE_RECORD_FAILED_ERROR_MESSAGE)
        # nothing else to do
        return
    try:
        await message.react(
            reaction=[
                types.ReactionTypeEmoji(emoji="👍"),
            ],
            is_big=True
        )
    except AiogramError as e:
        logger.error(f"Failed to react to user's message: {e}")


@router.message(~F.text)
async def non_text_message_handler(message: types.Message) -> None:
    """
        handles regular non-text messages, as they're currently not supported
    """
    await message.reply(NON_TEXT_MESSAGE_ERROR_MESSAGE)
    logger.info(f"non-text message type {message}")
