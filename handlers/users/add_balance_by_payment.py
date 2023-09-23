from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.addition_balance import AdditionBalance
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.yoomoney_method import create_transaction
from handlers.users.work_with_payments import check_payment_yoomoney
from handlers.users.check_payment_status import check_status
from data.config import TIME_TO_WAIT_PAYMENT_IN_SECONDS



@dp.callback_query_handler(Text(equals='add_balance'))
async def add_balance_by_payment(q: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=q.from_user.id, text='Выберите метод оплаты:',
                           reply_markup=keyboard_for_add_balance())
    await AdditionBalance.wait_method_payment.set()


@dp.callback_query_handler(state=AdditionBalance.wait_method_payment)
async def get_payment_method(q: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=q.from_user.id, text='Введите сумму, на которую хотите пополнить:')
    await state.update_data(payment_method=q.data)
    await AdditionBalance.next()


@dp.message_handler(state=AdditionBalance.wait_value_for_adding)
async def wait_value_to_adding(msg: Message, state: FSMContext):
    try:
        value = int(msg.text)
        payment_method = (await state.get_data())['payment_method']
        label, url = create_transaction(summ=value)
        await state.update_data(value=value, label=label)
        create_payment(user_id=msg.from_user.id, amount=value, payment_method=payment_method, label=label)
        message = f'Пополнение баланса на сумму {bold_text(value)}₽\n' \
                  f'Ссылка для оплаты: {hyper_text("ссылка", url)}\n\n' \
                  f'Цена указана с учётом комиссии'
        message = await msg.answer(text=message, reply_markup=keyboard_yoomoney_method(url))
        await AdditionBalance.next()
        scheduler_io.add_job(func=check_status, trigger='date', run_date=datetime.now() + timedelta(seconds=TIME_TO_WAIT_PAYMENT_IN_SECONDS),
                             args=(str(label), message.message_id), id=str(label))
        scheduler_io.start()
    except ValueError:
        await msg.answer('Значение должно быть числом')
        await state.finish()

# @dp.callback_query_handler(Text(equals='check_payment_yoomoney'), state=AdditionBalance.wait_confirm)
# async def confirm_balance_payment(q: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     label = data['label']
#     if await check_payment_yoomoney(label=label):
#         value = data['value']
#         add_balance(user_id=q.from_user.id, plus_balance=value)
#         balance = get_user_balance(user_id=q.from_user.id)
#         await bot.send_message(chat_id=q.from_user.id, text=f'Вы успешно пополнили баланс на сумму {bold_text(value)}₽\n\nВаш текущий баланс: {bold_text(balance)}₽')
#         await state.finish()
#     else:
#         await q.answer('Извините, оплата ещё не прошла, попробуйте подтвердить позже', show_alert=True)
