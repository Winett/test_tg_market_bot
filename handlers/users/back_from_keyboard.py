from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from handlers.users.callback_category import send_subcategories
from utils.keyboards import *
from database.work_with_sqlite3 import *


@dp.callback_query_handler(Text(contains='back_to_category'), state='*')
async def back(q: CallbackQuery, state: FSMContext):
    await state.finish()
    await send_categories_from_back(q=q, state=state)


async def send_categories_from_back(q: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text='Выберите категорию: ', chat_id=q.from_user.id, message_id=q.message.message_id,
                                reply_markup=keyboard_for_buy_item())


@dp.callback_query_handler(Text(equals='back_to_subcategory'), state='*')
async def send_subcategories_from_back(q: CallbackQuery, state: FSMContext):
    await send_subcategories_from_back(q=q, state=state)


async def send_subcategories_from_back(q: CallbackQuery, state: FSMContext):
    # await state.update_data(category_id=category)
    category_id = (await state.get_data())['category_id']
    await bot.edit_message_text(text='Выберите категорию:', chat_id=q.message.chat.id, message_id=q.message.message_id,
                                reply_markup=keyboard_for_callback_category(category_id=category_id))
