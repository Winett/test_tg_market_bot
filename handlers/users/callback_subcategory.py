from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy
from handlers.users import buy
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *


@dp.callback_query_handler(Text(startswith='subcategory'), state=Buy.pre_buy)
async def send_item(q: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_id = data['category_id']
    subcategory_id = get_id_from_subcategory_name(' '.join(q.data.split()[1:]))
    count_of_accounts = get_count_of_items(category_id=category_id, subcategory_id=subcategory_id)
    if count_of_accounts <= 10:
        max_keyboard_button = count_of_accounts
    else:
        max_keyboard_button = 11
    message = f"{bold_text('Товар')}: {get_name_from_category_id(category_id)} - {get_name_from_subcategory_id(subcategory_id)}\n" \
              f"{bold_text('Описание')}: {get_description_subcategory(subcategory_id)}\n" \
              f"{bold_text('Остаток')}: {count_of_accounts} шт.\n" \
              f"{bold_text('Цена')}: {get_price_subcategory(subcategory_id=subcategory_id)}₽\n\n" \
              f"Отправьте необходимое кол-во товара, либо нажмите на одну из кнопок ниже:"
    await Buy.pre_buy.set()
    await state.update_data(count_of_accounts=count_of_accounts)
    await state.update_data(category_id=category_id, subcategory_id=subcategory_id, message_id=q.message.message_id)
    await bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text=message, reply_markup=keyboard_for_callback_subcategory(max_keyboard_button))

@dp.message_handler(state=Buy.pre_buy)
async def get_count_account(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        count = int(msg.text)
        msg_id_for_delete = data.get('msg_id_for_delete', [])
        msg_id_for_delete.append(msg.message_id)
        if data['count_of_accounts'] < count:
            message = await msg.answer('Вы ввели слишком большое число. В наличии нет столько аккаунтов!', reply_markup=keyboard_delete_message())
            msg_id_for_delete.append(message.message_id)
            await state.update_data(msg_id_for_delete=msg_id_for_delete)
        else:
            await state.update_data(count=count, msg_id_for_delete=msg_id_for_delete)
            await buy.buy(msg, state)
    except ValueError:
        await msg.answer('Вы ввели не число')