from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from handlers.users.callback_category import send_subcategories
from utils.keyboards import *
from database.work_with_sqlite3 import *

@dp.callback_query_handler(Text(contains='Главная'), state='*')
async def main_from_keyboard(q: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(q.message.chat.id, q.message.message_id)
    await bot.send_message(text='Выберите категорию:', chat_id=q.message.chat.id, reply_markup=keyboard_start())



# async def send_subcategories_from_main(q: CallbackQuery):
#     await bot.edit_message_text(text='Выберите категорию:', chat_id=q.message.chat.id, message_id=q.message.message_id, reply_markup=gen_inline_buttons(list_of_name_buttons=all_category(), post_script=f'category', row_width=2))




