from aiogram.types import Message
from aiogram.filters import Filter


class ReplyBotFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.reply_to_message:
            if message.reply_to_message.from_user.is_bot:
                return True
        return False
