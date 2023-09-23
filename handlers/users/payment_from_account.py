from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Payment
from loader import dp, bot
from utils.keyboards import *
from database.work_with_sqlite3 import *
from handlers.users.work_with_payments import send_items_after_buying

@dp.callback_query_handler(Text(contains='payment_from_account'), state=Payment.Payment_data)
async def payment_from_account(q: CallbackQuery, state: FSMContext):
    user_balance = get_user_balance(q.from_user.id)
    await Payment.next()
    msg_id_for_delete = await bot.send_message(chat_id=q.from_user.id, text=f'У вас на балансе {user_balance}₽\n\nПодтвердите, пожалуйста, покупку по кнопке ниже', reply_markup=keyboard_confirm_buying_from_user_balance())
    await state.update_data(payment_method='payment_from_account', user_id=q.from_user.id, msg_id=[msg_id_for_delete.message_id, q.message.message_id], chat_id=q.from_user.id, user_balance=user_balance)



@dp.callback_query_handler(Text(equals='confirm_buying_from_user_balance'), state=Payment.confirm_buying)
async def confirm_buying_from_user_balance(q: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data['msg_id']
    chat_id = data['chat_id']
    total_sum = data['total_sum']
    user_balance = data['user_balance']
    for msg in msg_id:
        await bot.delete_message(chat_id=chat_id, message_id=msg)
    await state.finish()
    if user_balance >= total_sum:
        await send_items_after_buying(bot=bot, data=data)
    else:
        await bot.send_message(chat_id=q.message.chat.id, text='Вам не хватает денежных средств, пожалуйста, пополните свой баланс!', reply_markup=keyboard_start())
