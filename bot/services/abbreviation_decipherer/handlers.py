import random
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import config
from abbreviation_decipherer.abbreviation_decipherer import (
    adjf_noun_of_noun,
    get_deciphers,
    n_adjf_of_noun,
)
from abbreviation_decipherer.filters import RandomFilter
from utils.command_registry import register_command

register_command("/abbr {слово}", "Дать расшифровку сокращённого слова")
register_command("/blt {аббревиатура}", "Грубая расшифровка аббревиатуры с матом")

abbreviation_decipherer_router = Router()


@abbreviation_decipherer_router.message(
    RandomFilter(chance=0.06),
    F.chat.id.in_((config.CHAT_ID,)),
)
async def abbr_message_handler(msg: Message):
    """
    обрабатывает сообщение с некоторой вероятностью сообщения,
    из строки берётся одно случайное слово и ему даётся расшировка
    """
    msg_text = msg.text.lower()
    msg_text = re.sub(r"[^\w]", " ", msg_text).strip()
    words = set(msg_text.split())
    if not words:
        return
    variants = list()
    for w in words:
        if len(w) > 5:
            continue
        norm_word = w.strip()
        is_orig, corr_abbr, deciphers = get_deciphers(norm_word)
        if deciphers:
            variants.append((w, is_orig, corr_abbr, deciphers))
    if not variants:
        return

    random_abbr = random.choice(variants)
    random_decipher = random.choice(random_abbr[3])
    orig_abbr = random_abbr[0]
    is_orig = random_abbr[1]
    corr_abbr = random_abbr[2]

    if is_orig == 1:
        text = f'Пиши НЕ <b>"{orig_abbr}"</b>, a <b>"{random_decipher}"</b>'
    elif is_orig == 0:
        text = f'Тебе так лень написать <b>"{random_decipher}"</b> вместо <b>"{orig_abbr}"</b>?!'
    else:
        text = "Позовите Серёгу, мне плохо от ваших сокращений."
    await msg.reply(text)


@abbreviation_decipherer_router.message(Command("abbr"))
async def abbr_command_handler(msg: Message):
    """
    обрабатывает команду abbr, которая имеет аргумент строку
    из строки берётся одно случайное слово и ему даётся расшировка
    (подразумевается, что будет передаваться только одно слово)
    """
    msg_text = msg.text.lower()
    msg_text = re.sub("[^\w]", " ", msg_text).strip()
    words = set(msg_text.split())
    if not words:
        await msg.reply("Я не нашёл сокращений")
        return
    variants = list()
    for w in words:
        norm_word = w.strip()
        is_orig, corr_abbr, deciphers = get_deciphers(norm_word)
        if deciphers:
            variants.append((w, is_orig, corr_abbr, deciphers))
    if not variants:
        await msg.reply("Я не нашёл сокращений")
        return

    random_abbr = random.choice(variants)
    random_decipher = random.choice(random_abbr[3])
    orig_abbr = random_abbr[0]
    is_orig = random_abbr[1]
    corr_abbr = random_abbr[2]

    if is_orig == 1:
        text = f'Пиши НЕ <b>"{orig_abbr}"</b>, a <b>"{random_decipher}"</b>'
    elif is_orig == 0:
        text = f'Тебе так лень написать <b>"{random_decipher}"</b> вместо <b>"{orig_abbr}"</b>?!'
    else:
        text = "Позовите Серёгу, мне плохо от ваших сокращений."
    await msg.reply(text)


@abbreviation_decipherer_router.message(Command("blt"))
async def blt_command_handler(msg: Message):
    """
    комагда blt нужна чтобы ругаться матом
    """
    msg_text = msg.text.lower()
    abbr = msg_text.split()[1]
    if len(abbr) == 3:
        decipher = adjf_noun_of_noun(abbr)
    else:
        decipher = n_adjf_of_noun(abbr)
    if decipher:
        text = f'Пиши НЕ <b>"{abbr}"</b>, a <b>"{decipher}"</b>'
        await msg.reply(text)
    else:
        await msg.reply("Я хер знает что тебе надо")
