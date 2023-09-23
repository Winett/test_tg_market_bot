from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from data.config import for_user_history, time_utc_in_hours
from database.work_with_sqlite3 import *
from datetime import datetime, timedelta


@dp.callback_query_handler(Text(equals='buys'))
async def get_user_history(q: CallbackQuery):
    message = 'Ваши последние 10 покупок:'
    data = get_purchase_history_for_buttons(user_id=q.from_user.id)[::-1]
    if len(data) > 10:
        # delete_purchase_history(ids_history=list(map(lambda x: x[0], data[10:])))
        data = data[:10]
    await bot.send_message(chat_id=q.from_user.id, text=message, reply_markup=keyboard_history_buys(data))

@dp.callback_query_handler(Text(startswith='history_buys'))
async def user_buy_information(q: CallbackQuery):
    purchase_id = int(q.data.split()[-1])
    message = 'Информация о вашей покупке:\n'
    history = check_purchase_history(purchase_id=purchase_id)
    purchase_id = history[0]
    item_name = history[2]
    count = history[3]
    price_item = int(history[4])
    total_price = int(history[5])
    method = for_user_history.get(history[6], 'Метод не добавлен')
    date = datetime.fromisoformat(history[7]) + timedelta(hours=time_utc_in_hours)
    if date.minute < 10:
        minute = f'0{date.minute}'
    else:
        minute = date.minute
    message += f'{bold_text("ID")}: {code_text(purchase_id)}\n' \
               f'{bold_text("Наименование товара")}: {code_text(item_name)}\n\n' \
               f'{bold_text("Цена за штуку")}: {code_text(price_item) + " ₽"}\n' \
               f'{bold_text("Количество")}: {code_text(count)}\n' \
               f'{bold_text("Общая сумма")}: {code_text(total_price) + " ₽"}\n\n' \
               f'{bold_text("Оплачено")}: {code_text(method)}\n\n' \
               f'{bold_text("Дата оплаты")}: {code_text(f"{date.day}.{date.month}.{date.year} в {date.hour}:{minute}")}'
    await bot.send_message(chat_id=q.from_user.id, text=message, reply_markup=None)



