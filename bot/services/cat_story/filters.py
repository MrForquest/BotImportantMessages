from aiogram.filters import Filter
from aiogram.types import Message

import config


class ReplyBotFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.reply_to_message:
            if message.reply_to_message.from_user.is_bot:
                return True
        return False


class IsBotAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == config.BOT_ADMIN_ID
