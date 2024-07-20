from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from import_message_sorter.filters import ImportanceFilter
import config

important_message_sorter_router = Router()


@important_message_sorter_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я живая!")


@important_message_sorter_router.message(ImportanceFilter())
async def message_handler(msg: Message):
    forwarded_msg = await msg.bot.forward_message(
        chat_id=config.REPORT_CHANNEL_ID,
        from_chat_id=msg.chat.id,
        message_id=msg.message_id,
    )

    msg_url = msg.get_url(force_private=True)
    msg_text = f"Чат: {msg.chat.title}\nURL: {msg_url}"

    await msg.bot.send_message(
        config.REPORT_CHANNEL_ID,
        msg_text,
        reply_to_message_id=forwarded_msg.message_id,
    )


# TODO
"""
Так, ребят, скоро, важно, нужно, вместе, соберемся, в понедельник, на следующей неделе, поедем, пойдем, гулять, погулять
"""
