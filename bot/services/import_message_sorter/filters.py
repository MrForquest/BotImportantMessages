from aiogram.filters import Filter
from aiogram.types import Message

import config


class ImportanceFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        is_importance = False
        in_text = config.IN_TEXT

        if message.text:
            text = message.text.lower()
            # проверка ключевых слов и символов в сообщении
            if any([substring in text for substring in in_text]):
                is_importance = True
        # проверка наличия документа
        if message.document:
            is_importance = True

        return is_importance
