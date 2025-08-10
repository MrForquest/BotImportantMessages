from typing import Dict

command_registry: Dict[str, str] = {}


def register_command(cmd: str, desc: str):
    command_registry[cmd] = desc
