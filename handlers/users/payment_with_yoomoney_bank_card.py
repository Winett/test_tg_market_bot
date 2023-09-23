from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Payment, Check_payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.yoomoney_method import create_transaction
from handlers.users.check_payment_status import check_status
from data.config import TIME_TO_WAIT_PAYMENT_IN_SECONDS


@dp.callback_query_handler(Text(contains='yoomoney_method'), state=Payment.Payment_data)
async def payment_with_yoomoney_bank_card(q: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_id = data['category_id']
    subcategory_id = data['subcategory_id']
    count = data['count']
    total_sum = data['total_sum']
    message_id = data['message_id']
    price_per_item = data['price_per_item']
    await state.finish()
    label, url = create_transaction(total_sum)
    create_payment(user_id=q.from_user.id, amount=total_sum, payment_method='yoomoney_method', label=label)
    scheduler_io.add_job(func=check_status, trigger='date', run_date=datetime.now() + timedelta(seconds=TIME_TO_WAIT_PAYMENT_IN_SECONDS),
                         args=(str(label), q.message.message_id), id=str(label))
    scheduler_io.start()
    # scheduler_io.add_job()
    await Check_payment.wait_confirmation.set()
    await state.update_data(label=label, category_id=category_id, subcategory_id=subcategory_id, count=count, total_sum=total_sum, message_id=q.message.message_id, user_id=q.message.chat.id, payment_method='yoomoney_method', price_per_item=price_per_item)
    message = f'Покупка {count} шт. {bold_text(f"{get_name_from_category_id(category_id)} - {get_name_from_subcategory_id(subcategory_id)}")}\n' \
              f'Ссылка для оплаты: {hyper_text("ссылка", url)}\n\n' \
              f'Цена указана с учётом комиссии'
    await bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text=message, reply_markup=keyboard_yoomoney_method(url))