from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *


@dp.callback_query_handler(Text(startswith='buy'), state=Buy.pre_buy)
async def buy(q: CallbackQuery | Message, state: FSMContext):
    data: dict = await state.get_data()
    # if 'count' not in await state.get_data():
    category_id = data.get("category_id", 0)
    subcategory_id = data.get('subcategory_id', 0)
    if isinstance(q, CallbackQuery):
        count = q.data.split()[-1]
    else:
        count = data.get('count', 0)
    message_id = data.get('message_id', 0)
    messages_for_delete = data.get('msg_id_for_delete', [])
    for msg_id in messages_for_delete:
        await bot.delete_message(chat_id=q.chat.id, message_id=msg_id)
    # else:
    #     category_id = data.get("category_id", 0)
    #     subcategory_id = data.get('subcategory_id', 0)
    #     count = data.get('count', 0)
    #     message_id = data.get('message_id', 0)
    #     await bot.delete_message(chat_id=q.chat.id, message_id=q.message_id)
    price_per_item = int(get_price_subcategory(subcategory_id))
    total_sum = price_per_item * int(count)
    await state.finish()
    await Payment.Payment_data.set()
    await state.update_data(category_id=category_id, subcategory_id=subcategory_id, count=count, total_sum=total_sum, message_id=message_id, price_per_item=price_per_item)
    message = f"Ваш заказ: \n" \
              f"{bold_text('Товар')}: {get_name_from_category_id(category_id)} - {get_name_from_subcategory_id(subcategory_id)} \n" \
              f"{bold_text('Сумма покупки')}: {code_text(f'{total_sum}₽')} за {count} шт.\n\n" \
              f"Выберите способ оплаты: "
    if isinstance(q, CallbackQuery):
        await bot.edit_message_text(text=message, chat_id=q.message.chat.id, message_id=q.message.message_id, reply_markup=keyboard_for_payment())
    else:
        await bot.edit_message_text(text=message, chat_id=q.chat.id, message_id=message_id, reply_markup=keyboard_for_payment())