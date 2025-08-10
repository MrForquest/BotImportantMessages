import asyncio
import collections
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares import HistoryMiddleware, MultiHandlerMiddleware
from services.abbreviation_decipherer.handlers import abbreviation_decipherer_router
from services.cat_story.handlers import cat_story_router
from services.import_message_sorter.handlers import important_message_sorter_router
from services.utils.handlers import utils_router

import config


async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp["history"] = collections.defaultdict(lambda: collections.deque(maxlen=30))
    dp.include_router(utils_router)
    dp.include_router(important_message_sorter_router)
    dp.include_router(abbreviation_decipherer_router)
    dp.include_router(cat_story_router)
    dp.update.outer_middleware(HistoryMiddleware())
    dp.update.outer_middleware(MultiHandlerMiddleware(dp))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
