from os import remove

from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.add_accounts import AddAccounts
from loader import dp, bot
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.custom_filters import IsAdmin
from utils.markdown import *


@dp.callback_query_handler(IsAdmin(), Text(contains='add_items'))
async def add_items(q: CallbackQuery, state: FSMContext):
    await AddAccounts.select_category.set()
    await bot.send_message(chat_id=q.from_user.id, text='Выберите, пожалуйста, для какой катеории вы бы хотели добавить товар:', reply_markup=gen_inline_buttons(list_of_name_buttons=all_category(), post_script='add_to_category', last_button=['❌ Отмена', 'cancel'], use_as_callback_data_next_value_for_last_button=True))


@dp.callback_query_handler(IsAdmin(), Text(startswith='add_to_category'), state=AddAccounts.select_category)
async def add_to_category(q: CallbackQuery, state: FSMContext):
    data = q.data.split()
    category_id = get_id_from_category_name(data[-1])
    await state.update_data(category_id=category_id)
    await AddAccounts.next()
    await bot.edit_message_text(text='Выберите, пожалуйста, для какой подкатеории вы бы хотели добавить товар:',
                                chat_id=q.message.chat.id, message_id=q.message.message_id, reply_markup=gen_inline_buttons(list_of_name_buttons=all_subcategory(category_id), post_script='add_to_subcategory', last_button=['❌ Отмена', 'cancel'], use_as_callback_data_next_value_for_last_button=True))


@dp.callback_query_handler(IsAdmin(), Text(startswith='add_to_subcategory'), state=AddAccounts.select_subcategory)
async def add_to_subcategory(q: CallbackQuery, state: FSMContext):
    data = q.data.split()
    subcategory_id = get_id_from_subcategory_name(' '.join(data[1:]))
    await state.update_data(subcategory_id=subcategory_id)
    await AddAccounts.next()
    await bot.edit_message_text(text=f'Выберите, пожалуйста, тип загружаемых данных',
                                chat_id=q.message.chat.id, message_id=q.message.message_id, reply_markup=keyboard_type_of_adding_data())


@dp.callback_query_handler(Text(startswith='type_of_data'), state=AddAccounts.select_type_accounts)
async def add_account_type(q: CallbackQuery, state: FSMContext):
    type = q.data.split()[-1]
    await state.update_data(type=type)
    await AddAccounts.next()
    await bot.edit_message_text(
        text=f'Отправите, пожалуйста, данные в формате {code_text(type)} сообщением или txt файлом',
        chat_id=q.message.chat.id, message_id=q.message.message_id,
        reply_markup=keyboard_cancel())

@dp.message_handler(IsAdmin(), content_types=[ContentType.DOCUMENT, ContentType.TEXT], state=AddAccounts.wait_data)
async def add_accounts(msg: Message, state: FSMContext):
    data = await state.get_data()
    category_id = data['category_id']
    subcategory_id = data['subcategory_id']
    type = data['type']
    accounts = []
    if msg.content_type == ContentType.TEXT:
        for line in msg.text.split('\n'):
            try:
                login, password, access_token = None, None, None
                match len(type.split(':')):
                    case 1:
                        access_token = line
                    case 2:
                        login, password = line.split(':')
                    case 3:
                        login, password, access_token = line.split(':')
                accounts.append((category_id, subcategory_id, login, password, access_token))
                # add_account(category_id=category_id, subcategory_id=subcategory_id, login=login, password=password)
            except ValueError:
                await msg.answer('Вы ввели данные некоректно, введите их ещё раз!', reply_markup=keyboard_cancel())
                return
    elif msg.content_type == ContentType.DOCUMENT:
        await bot.download_file_by_id(file_id=msg.document.file_id, destination=f'datafile_{msg.from_user.id}_{category_id}_{subcategory_id}.txt')
        with open(f'datafile_{msg.from_user.id}_{category_id}_{subcategory_id}.txt') as f:
            for line in f.readlines():
                try:
                    login, password, access_token = None, None, None
                    match len(type.split(':')):
                        case 1:
                            access_token = line
                        case 2:
                            login, password = line.split(':')
                        case 3:
                            login, password, access_token = line.split(':')
                    accounts.append((category_id, subcategory_id, login, password, access_token))
                except ValueError:
                    await msg.answer('В файле данные не корректны, пожалуйста, перепроверьте файл!',
                                     reply_markup=keyboard_cancel())
                    return
                finally:
                    remove(f'datafile_{msg.from_user.id}_{category_id}_{subcategory_id}.txt')
    add_many_accounts(accounts, type=type)
    await state.finish()
    await msg.answer('Данные успешно добавлены!')