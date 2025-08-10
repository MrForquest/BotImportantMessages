from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.command_registry import command_registry, register_command

register_command("/help", "Показать список доступных команд")

utils_router = Router()


@utils_router.message(Command("help"))
async def cmd_help(msg: Message):
    lines = ["Доступные команды:"]
    for cmd, desc in sorted(command_registry.items()):
        lines.append(f"{cmd} — {desc}")
    await msg.reply("\n\n".join(lines))
