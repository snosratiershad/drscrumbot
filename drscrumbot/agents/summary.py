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
    Agents related to summarization
"""
import logging

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from drscrumbot.config import config
from drscrumbot.schemas import Summary
from drscrumbot.agents.deps import SummaryAgentDeps
from drscrumbot.database.connection import db_connection
from drscrumbot.database.models import Update
from drscrumbot.utils.instructions import SUMMARY_AGENT_INSTRUCTIONS

logger: logging.Logger = logging.getLogger(__name__)
model: OpenAIChatModel = OpenAIChatModel(
    model_name="gpt-5-nano",
    provider=OpenAIProvider(api_key=config.openai_api_key.get_secret_value())
)

agent: Agent[SummaryAgentDeps, Summary] = Agent[
    SummaryAgentDeps,
    Summary
](
    model=model,
    output_type=Summary,
    instructions=SUMMARY_AGENT_INSTRUCTIONS,
    deps_type=SummaryAgentDeps,
    name="DrScrum",
)


@agent.instructions
def add_user_info(ctx: RunContext[SummaryAgentDeps]) -> str:
    return f"user info: first name: {ctx.deps.user.first_name}" + \
        f"last name: {ctx.deps.user.last_name}"


@agent.instructions
def add_updates_info(ctx: RunContext[SummaryAgentDeps]) -> str:
    return "updates: \n" + "\n".join(
        list(map(lambda u: f"{u.date} - {u.text}", ctx.deps.updates))
    )


@agent.instructions
async def add_last_update_report(ctx: RunContext[SummaryAgentDeps]) -> str:
    try:
        async with db_connection.get_session() as session:
            latest_update: Update | None = (await session.execute(
                select(Update).
                where(Update.user_id == ctx.deps.user.telegram_id).
                order_by(Update.created_at.desc()).
                limit(1)
            )).scalar_one_or_none()
            if latest_update:
                return f"last update:\n{latest_update.text}"
            else:
                return "last update: No recent update"
    except DatabaseError as e:
        logger.error(f"Failed when fetching recent update: {e}")
        return "last: No recent update"
