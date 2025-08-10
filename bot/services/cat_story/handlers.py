import collections
import os
import pathlib
from typing import Dict, Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import formatting
from openai import OpenAI

import config
from cat_story.filters import IsBotAdmin, ReplyBotFilter
from utils.command_registry import register_command

MODEL_NAME = "gemini-2.5-flash"
GPT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

DEFAULT_PROMPTS = {
    "rude_prompt": {
        "filename": "rude_prompt.txt",
        "desc": "Очень грубый промпт с матами и оскорблениями.",
    },
    "right_friend_prompt": {
        "filename": "right_friend_prompt.txt",
        "desc": "Промпт для друга с крайне правыми взглядами",
    },
    "friend_prompt": {
        "filename": "friend_prompt.txt",
        "desc": "Промпт для подруги, с которой интересно болтать",
    },
}

current_dir = pathlib.Path(__file__).resolve().parent
cat_story_router = Router()
gpt_client = OpenAI(
    api_key=config.GPT_TOKEN,
    base_url=GPT_BASE_URL,
)


def get_prompt_by_name(prompt_name: str) -> Optional[str]:
    prompt_obj = DEFAULT_PROMPTS.get(prompt_name, None)
    if prompt_obj is None:
        return None
    path = current_dir / os.path.join("prompts", prompt_obj["filename"])
    with open(path, "r", encoding="utf-8") as f:
        prompt_ = f.read()
    return prompt_


system_prompt = _p if (_p := get_prompt_by_name("friend_prompt")) else ""


def serialize_chat_history(messages, chat_history):
    for ch_msg in chat_history:
        msg_data = list()
        if ch_msg["username"] == "markisa_system":
            f_msg = {"role": "assistant"}
        else:
            name = ",".join((ch_msg["username"], ch_msg["full_name"]))
            f_msg = {"role": "user"}
            msg_data.append("[Отправитель: {}]".format(name))

        if ch_msg["content_type"] != "text":
            msg_data.append("[К сообщению приложено {}]".format(ch_msg["content_type"]))

        if ch_msg["is_fwrd_msg"]:
            fwrd_name = ",".join((ch_msg["username"], ch_msg["full_name"]))
            msg_data.append(
                "[Это сообщение было переслано из {} {}]".format(
                    ch_msg["fwrd_msg_data"]["type"], fwrd_name
                )
            )
        msg_data.append(ch_msg["text"])
        msg_text = "\n".join(msg_data)
        f_msg["content"] = msg_text
        messages.append(f_msg)
    return messages


@cat_story_router.message(Command("story"))
@cat_story_router.message(ReplyBotFilter())
async def cat_story(msg: Message, history: Dict[int, collections.deque]):
    chat_history = history[msg.chat.id]
    messages = [{"role": "system", "content": system_prompt}]
    messages = serialize_chat_history(messages, chat_history)
    print(messages)
    completion = gpt_client.chat.completions.create(model=MODEL_NAME, messages=messages)
    ai_answer = completion.choices[0].message.content
    ai_data = {
        "username": "markisa_system",
        "full_name": "Механическая Маркиса",
        "content_type": "text",
        "is_fwrd_msg": False,
        "text": ai_answer,
    }
    chat_history.append(ai_data)
    await msg.reply(completion.choices[0].message.content)


@cat_story_router.message(Command("full_clean"), IsBotAdmin())
async def clean_history(msg: Message, history: Dict[int, collections.deque]):
    history.clear()
    await msg.reply("Вся история удалена.")


@cat_story_router.message(Command("set_system_prompt"), IsBotAdmin())
async def set_system_prompt(msg: Message):
    global system_prompt
    system_prompt = msg.text.replace("/set_system_prompt", "")

    await msg.reply("Новый системный промпт установлен.")


@cat_story_router.message(Command("set_named_prompt"), IsBotAdmin())
async def set_system_prompt(msg: Message):
    global system_prompt
    prompt_name = msg.text.replace("/set_named_prompt", "").strip()
    new_prompt = get_prompt_by_name(prompt_name)
    if new_prompt is None:
        await msg.reply(f'Промпт с именем "{prompt_name}" не найден.')
    else:
        system_prompt = new_prompt
        await msg.reply("Новый системный промпт установлен.")


@cat_story_router.message(Command("get_list_def_prompts"))
async def get_list_prompts(msg: Message):
    lines = []  # ["Доступные промпты:"]
    for prompt_name, prompt_dict in sorted(DEFAULT_PROMPTS.items()):
        content = formatting.Text(
            formatting.Bold(prompt_name), " - ", prompt_dict["desc"]
        )
        lines.append(content)
    await msg.reply(**formatting.as_list(*lines, sep="\n\n").as_kwargs())


@cat_story_router.message(Command("get_current_prompt"), IsBotAdmin())
async def get_current_prompt(msg: Message):
    global system_prompt
    await msg.reply("Текущий системный промпт:\n{}".format(system_prompt))


register_command("/story {text}", "Генерация ответа на основе истории чата и промпта")
register_command(
    "/full_clean",
    "Удалить всю историю сообщений для всех чатов (только для владельца бота)",
)
register_command(
    "/set_system_prompt {текст}",
    "Установить системный промпт вручную (только для владельца бота)",
)
register_command(
    "/set_named_prompt {имя}",
    "Установить системный промпт по имени (из файла) (только для владельца бота)",
)
register_command(
    "/get_list_def_prompts", "Показать список доступных встроенных промптов"
)
register_command(
    "/get_current_prompt",
    "Показать текущий системный промпт (только для владельца бота)",
)
