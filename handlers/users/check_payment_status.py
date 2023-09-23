from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Bot

from states.addition_balance import AdditionBalance
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.yoomoney_method import create_transaction
from handlers.users.work_with_payments import check_payment_yoomoney

async def check_status(label: str, message_id):
    id, user_id, status = get_payment_status(label=str(label))
    if status == 'waiting':
        await bot.delete_message(chat_id=user_id, message_id=message_id)
        change_status_in_payment_history(label=label, new_status='cancel')
        await bot.send_message(chat_id=user_id, text=f'Платёж #<code>{id}</code> был отменён')
