from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message, Update


# Middleware definition
class MultiHandlerMiddleware(BaseMiddleware):
    def __init__(self, dispatcher: Dispatcher):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        for router in data["dispatcher"].sub_routers:
            for r_handler in router.message.handlers:
                is_ok = all(
                    [await f.call(event.message, **data) for f in r_handler.filters]
                )
                if is_ok:
                    await r_handler.call(event.message, **data)


def parse_forwarded_message(forward_origin) -> Any:
    origin_type = forward_origin.type
    forwarded_msg_data = {"type": origin_type.value, "username": "", "full_name": ""}

    if origin_type == "user":
        forwarded_msg_data["full_name"] = forward_origin.sender_user.full_name
        forwarded_msg_data["username"] = forward_origin.sender_user.username
    elif origin_type == "hidden_user":
        forwarded_msg_data["full_name"] = "full_name_is_hidden"
        forwarded_msg_data["username"] = forward_origin.sender_user_name
    elif origin_type == "chat":
        forwarded_msg_data["full_name"] = forward_origin.sender_chat.full_name
        forwarded_msg_data["username"] = forward_origin.sender_chat.username
    elif origin_type == "channel":
        forwarded_msg_data["full_name"] = forward_origin.chat.full_name
        forwarded_msg_data["username"] = forward_origin.chat.username
    else:
        raise TypeError(f"Unknown message origin: {origin_type}")

    return forwarded_msg_data


class HistoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if event.message:
            history = data["history"]
            text = ""
            is_fwrd_msg = False
            fwrd_msg_data = {}
            if event.message.forward_origin is not None:
                fwrd_msg_data = parse_forwarded_message(event.message.forward_origin)
                is_fwrd_msg = True
            if event.message.text is not None:
                text = event.message.text
            elif event.message.caption is not None:
                text = event.message.caption

            username = event.message.from_user.username
            full_name = event.message.from_user.full_name
            msg_data = {
                "username": username,
                "full_name": full_name,
                "text": text,
                "content_type": event.message.content_type.value,
            }

            if is_fwrd_msg:
                msg_data["is_fwrd_msg"] = True
                msg_data["fwrd_msg_data"] = fwrd_msg_data
            else:
                msg_data["is_fwrd_msg"] = False

            print(msg_data)
            history[event.message.chat.id].append(msg_data)

        return await handler(event, data)
