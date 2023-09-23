from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *


@dp.callback_query_handler(Text(equals='delete_message'), state='*')
async def delete_message(q: CallbackQuery):
    await bot.delete_message(chat_id=q.message.chat.id, message_id=q.message.message_id)