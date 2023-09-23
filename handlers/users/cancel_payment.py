from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Check_payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.yoomoney_method import create_transaction, operation_history
from handlers.users.payment_from_account import payment_from_account


@dp.callback_query_handler(Text(contains='cancel_payment'), state='*')
async def cancel_payment(q: CallbackQuery, state: FSMContext):
    ...