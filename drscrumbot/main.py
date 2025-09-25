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
    main module executing the application
"""
import logging
import sys

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.types import User
from aiogram.client.default import DefaultBotProperties

from drscrumbot.config import config
from drscrumbot.handlers import start_router, message_router, myupdates_router

logging.basicConfig(
    level=logging.INFO if not config.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger: logging.Logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """
        performs startup actions
    """
    bot_info: User = await bot.get_me()
    logging.info(f"starting {bot_info.username}...")


async def on_shutdown(bot: Bot):
    """
        performs gracefull shutdown

        closes all bot sessions
    """
    logging.info("shutting down...")
    await bot.session.close()
    logging.info("shutdown completed.")


async def main():
    """
        main function creates bot and dipatcher instance and starts polling
    """
    bot: Bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(protect_content=True)
    )

    dp: Dispatcher = Dispatcher(disable_fsm=True)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(start_router)
    dp.include_router(message_router)
    dp.include_router(myupdates_router)

    logger.info("starting polling...")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=["message"]
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    uvloop.run(main())
