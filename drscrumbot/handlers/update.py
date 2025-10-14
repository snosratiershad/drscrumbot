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
   handler routing for `/update`
"""
import logging

import httpx
from aiogram import Router, F, types
from aiogram.filters import Command, and_f
from aiogram.exceptions import AiogramError
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy import select, Result, Select
from sqlalchemy.exc import DatabaseError
from pydantic_ai.run import AgentRunResult

from drscrumbot.database import db_connection
from drscrumbot.database.models import Message, Update
from drscrumbot.agents import summary_agent
from drscrumbot.agents.deps import SummaryAgentDeps
from drscrumbot.schemas import (
    User as UserSchema,
    Update as UpdateSchema,
    Summary
)
from drscrumbot.utils.messages import UPDATE_MESSAGE, NOUPDATE_MESSAGE

logger: logging.Logger = logging.getLogger(__name__)
router: Router = Router()


@router.message(and_f(Command("update"), F.from_user))
async def update_handler(message: types.Message) -> None:
    """
      handler for `/update` command

      replies a list of updates from user messages with time
    """
    # As from_user is already filtered in router and is'nt None
    # The empty from_user is probably because of messages sent in a channel
    assert message.from_user
    # TODO: search why it's optional
    assert message.bot
    try:
        async with db_connection.get_session() as session:
            # state of update is currently simply handled by assuming user only
            # wants update of messages later from the last update.
            latest_update: Update | None = (await session.execute(
                select(Update).
                where(Update.user_id == message.from_user.id).
                order_by(Update.created_at.desc()).
                limit(1)
            )).scalar_one_or_none()
            if not latest_update:
                stmt: Select[Message] = (
                    select(Message).
                    where(Message.from_user_id == message.from_user.id).
                    order_by(Message.date)
                )
            else:
                stmt: Select[Message] = (
                    select(Message).
                    where(Message.created_at > latest_update.created_at).
                    where(Message.from_user_id == message.from_user.id).
                    order_by(Message.date)
                )
            result: Result = await session.execute(stmt)
            # TODO: we should limit the number of messages and handle it
            # statefully
            messages: list[Message] = result.scalars().all()
            if messages:
                updates: list[UpdateSchema] = list(
                    map(
                        lambda m: UpdateSchema(text=m.text, date=m.date),
                        messages
                    )
                )
                user: UserSchema = UserSchema(
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name
                )
                async with ChatActionSender(
                    bot=message.bot,
                    chat_id=message.chat.id,
                ):
                    async with httpx.AsyncClient() as client:
                        deps: SummaryAgentDeps = SummaryAgentDeps(
                            http_client=client,
                            updates=updates,
                            user=user
                        )
                        result: AgentRunResult[Summary] = await summary_agent.run(
                            deps=deps
                        )
                        summary: Summary = result.output
                update_text: str = UPDATE_MESSAGE.format(
                    last_day_i_did=summary.last_day_i_did,
                    today_i_will_do=summary.today_i_will_do,
                    any_blockers=summary.any_blockers
                )
                # TODO: we should store segments as well as final message
                update: Update = Update(
                    user_id=message.from_user.id,
                    text=update_text,
                    messages=messages
                )
                session.add(update)
                await session.commit()
                await message.reply(update_text)
            else:
                await message.reply(NOUPDATE_MESSAGE)

    except (AiogramError, DatabaseError, httpx.HTTPError) as e:
        logger.error(f"Error on generating user update: {e}")
