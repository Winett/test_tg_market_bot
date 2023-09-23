from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.buy_state import Buy
from utils.keyboards import *
from database.work_with_sqlite3 import *

@dp.callback_query_handler(Text(startswith='category'))
async def send_subcategories(q: CallbackQuery, state: FSMContext):
    category = q.data.split(' ')[1]
    await Buy.pre_buy.set()
    category = get_id_from_category_name(category)
    await state.update_data(category_id=category)
    await bot.edit_message_reply_markup(chat_id=q.message.chat.id, message_id=q.message.message_id, reply_markup=keyboard_for_callback_category(category_id=category))
