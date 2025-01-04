from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message, Update
from typing import Callable, Awaitable, Dict, Any


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
                is_ok = all([await f.call(event.message, **data) for f in r_handler.filters])
                if is_ok:
                    await r_handler.call(event.message, **data)
