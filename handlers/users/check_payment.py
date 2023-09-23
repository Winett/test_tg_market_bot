from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Check_payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from handlers.users.work_with_payments import check_payment_yoomoney
from utils.yoomoney_method import create_transaction, operation_history
from handlers.users.payment_from_account import payment_from_account
from handlers.users.work_with_payments import send_items_after_buying, send_balance_after_addition_balance


@dp.callback_query_handler(Text(startswith='check_payment_yoomoney'), state='*')
async def check_payment(q: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    label = data['label']
    # label = 'fe170e77-3127-4e4c-8681-8e5c860ca692'
    if await check_payment_yoomoney(label=label):
        scheduler_io.remove_job(job_id=str(label))
        change_status_in_payment_history(label=str(label), new_status='paid')
        if 'value' in data:
            value = data['value']
            data.update(user_id=q.from_user.id)
            await send_balance_after_addition_balance(bot=bot, data=data)
            await state.finish()
        else:
            await bot.delete_message(chat_id=q.from_user.id, message_id=q.message.message_id)
            await send_items_after_buying(bot=bot, data=data)
    else:
        await q.answer('Извините, оплата ещё не прошла, попробуйте подтвердить позже', show_alert=True)