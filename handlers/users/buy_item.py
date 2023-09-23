from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from loader import dp
from utils.keyboards import *
from database.work_with_sqlite3 import *

@dp.message_handler(Text('Купить товар'))
async def buy_item(msg: Message):
    await msg.answer('Выберите категорию:', reply_markup=keyboard_for_buy_item())