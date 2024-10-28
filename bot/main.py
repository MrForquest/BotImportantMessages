import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from services.import_message_sorter.handlers import important_message_sorter_router
from services.abbreviation_decipherer.handlers import abbreviation_decipherer_router
from services.cat_story.handlers import cat_story


from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(important_message_sorter_router)
    dp.include_router(abbreviation_decipherer_router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(cat_story, 'cron', hour=21, minute=4)
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())