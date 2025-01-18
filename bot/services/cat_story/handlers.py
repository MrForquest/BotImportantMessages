from pathlib import Path
import random

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from openai import OpenAI

import config
from cat_story.filters import ReplyBotFilter

# from apscheduler.schedulers.asyncio import AsyncIOScheduler

current_dir = Path(__file__).resolve().parent

cat_story_router = Router()
client = OpenAI(api_key=config.CHATGPT_KEY)

rude_prompt_file = open(current_dir / "rude_prompt.txt", "r", encoding="utf-8")
rude_prompt = rude_prompt_file.read()
rude_prompt_file.close()
kind_prompt_file = open(current_dir / "kind_prompt.txt", "r", encoding="utf-8")
kind_prompt = kind_prompt_file.read()
kind_prompt_file.close()
compliments_file = open(current_dir / "compliments.txt", "r", encoding="utf-8")
compliments = compliments_file.readlines()
compliments_file.close()
names_file = open(current_dir / "names.txt", "r", encoding="utf-8")
kind_names = names_file.readlines()
names_file.close()


def get_rude_prompt(msg):
    return rude_prompt


def get_kind_prompt(msg):
    text = msg.text.replace("/kstory", "")
    str_compliments = "".join(random.choices(compliments, k=4))
    str_names = "".join(random.choices(kind_names, k=4))

    prompt = kind_prompt.format(compliments=str_compliments, names=str_names)
    return prompt


@cat_story_router.message(Command("story"))
async def cat_story(msg: Message):
    text = msg.text.replace("/story", "")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": get_rude_prompt()},
            {
                "role": "user",
                "content": text
            }
        ]
    )
    await msg.reply(completion.choices[0].message.content)


@cat_story_router.message(ReplyBotFilter())
async def cat_reply(msg: Message):
    text = msg.text.replace("/story", "")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": get_kind_prompt(msg)},
            {
                "role": "assistant",
                "content": msg.reply_to_message.text
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    await msg.reply(completion.choices[0].message.content)


@cat_story_router.message(Command("kstory"))
async def cat_kind(msg: Message):
    text = msg.text.replace("/story", "")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": get_kind_prompt(msg)},
            {
                "role": "user",
                "content": text
            }
        ]
    )
    await msg.reply(completion.choices[0].message.content)
