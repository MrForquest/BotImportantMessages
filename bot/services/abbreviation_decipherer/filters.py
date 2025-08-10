import random

from aiogram.filters import Filter
from aiogram.types import Message


class RandomFilter(Filter):
    """
    сообщение будет обработано с вероятностью chance,
    минимум сообщений между срабатываниями min_msgs
    """

    def __init__(self, chance=0.08, min_msgs=20):
        self.chance = chance
        self.min_msgs = min_msgs
        self.msg_counters = dict()

    async def __call__(self, message: Message) -> bool:
        chat_id = message.chat.id
        msg_count = self.msg_counters.get(chat_id, 0)
        msg_count += 1
        if msg_count > 20:
            if random.random() < self.chance:
                self.msg_counters[chat_id] = 0
                return True

        self.msg_counters[chat_id] = msg_count
        return False
