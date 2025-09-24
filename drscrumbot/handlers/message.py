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

from drscrumbot.utils.messages import NON_TEXT_MESSAGE_ERROR_MESSAGE

logger: logging.Logger = logging.getLogger(__name__)

router: Router = Router()


@router.message(F.text & ~F.text.startswith("/"))
def message_handler(message: types.Message):
    """
        handles regular text messages
    """
    pass


@router.message(~F.text)
async def non_text_message_handler(message: types.Message):
    """
        handles regular non-text messages, as they're currently not supported
    """
    await message.reply(NON_TEXT_MESSAGE_ERROR_MESSAGE)
    logger.info(f"non-text message type {message}")
