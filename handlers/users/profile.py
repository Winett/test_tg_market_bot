from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from loader import dp
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from data.config import admins_id

@dp.message_handler(Text(startswith='Профиль'))
async def profile(msg: Message):
    message = f'👤 Username: @{msg.from_user.username}\n' \
              f'🆔 Telegram ID: {code_text(msg.from_user.id)}\n\n' \
              f'💰 Баланс: {get_user_balance(msg.from_user.id)}₽'
    if msg.from_user.id in admins_id:
        await msg.answer(text=message, reply_markup=keyboard_profile_admins())
    else:
        await msg.answer(message, reply_markup=keyboard_profile())