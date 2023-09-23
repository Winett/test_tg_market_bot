from os import remove

from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.work_with_category import EditCategory, AddCategory
from loader import dp, bot
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.custom_filters import IsAdmin
from utils.markdown import *

@dp.callback_query_handler(Text(equals='add_edit_category'))
async def work_with_category(q: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=q.from_user.id, text='Выберите, что вы хотите сделать с категорией', reply_markup=keyboard_work_with_category())

@dp.callback_query_handler(Text(equals='edit_category'))
async def edit_category(q: CallbackQuery, state: FSMContext):
    await EditCategory.wait_category_for_editing.set()
    await bot.edit_message_text(text='Выберите категорию, для которой хотите сменить название:', chat_id=q.from_user.id, message_id=q.message.message_id,  reply_markup=gen_inline_buttons(list_of_name_buttons=all_category(), post_script='', use_in_callback_data_name_of_button=True))

@dp.callback_query_handler(state=EditCategory.wait_category_for_editing)
async def category_for_editing(q: CallbackQuery, state: FSMContext):
    await state.update_data(category_for_editing=q.data, message_id=q.message.message_id)
    await bot.edit_message_text(text='Введите новое название категории:', chat_id=q.from_user.id, message_id=q.message.message_id)
    await EditCategory.next()

@dp.message_handler(state=EditCategory.wait_new_category_name)
async def new_name_category(msg: Message, state: FSMContext):
    data = await state.get_data()
    old_category_name = data['category_for_editing'].strip()
    message_id = data['message_id']
    change_name_category(msg.text, get_id_from_category_name(old_category_name))
    await bot.edit_message_text(text=f'Вы успешно сменили название категории с {code_text(old_category_name)} на {code_text(msg.text)}', chat_id=msg.from_user.id, message_id=message_id)
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await state.finish()


@dp.callback_query_handler(Text(equals='add_category'))
async def add_new_category(q: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=q.from_user.id, message_id=q.message.message_id, text='Отправьте название новой категории')
    await AddCategory.wait_new_category.set()
    await state.update_data(message_id=q.message.message_id)

@dp.message_handler(state=AddCategory.wait_new_category)
async def name_of_category_to_add(msg: Message, state: FSMContext):
    msg_id = (await state.get_data())['message_id']
    new_category = msg.text
    add_category(new_category)
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text=f'Вы успешно добавили новую категорию с названием {code_text(new_category)}')
    await state.finish()