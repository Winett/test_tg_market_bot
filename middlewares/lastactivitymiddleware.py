from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from database.work_with_sqlite3 import check_user_in_database, update_user_last_activity, update_username


class LastActivityMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if check_user_in_database(message.from_user.id):
            update_user_last_activity(message.from_user.id)
            update_username(user_id=message.from_user.id, user_name=message.from_user.username)
