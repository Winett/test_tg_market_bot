from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins_id


class IsAdmin(BoundFilter):
    async def check(self, msg: types.Message):
        return msg.from_user.id in admins_id
