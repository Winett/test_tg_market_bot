from loguru import logger
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import FSMContext

class LoggingMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        logger.info(f"Received message from {message.from_user.username}({message.chat.id}): {message.text}")

    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        logger.info(f"Received callback query from {cq.from_user.username}({cq.message.chat.id}): {cq.data}")
