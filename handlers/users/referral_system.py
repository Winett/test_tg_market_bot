from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.buy_state import Buy, Payment
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from data.config import referral_percent
from database.work_with_sqlite3 import *


@dp.callback_query_handler(Text(equals='referral_system'))
async def referrals(q: CallbackQuery):
    referral, earning = get_referrals_and_earning(q.from_user.id)
    message = f'{bold_text("Реферальная программа")}\n' \
              'Если человек перейдёт по вашей ссылке, то он станет вашим рефералом\n' \
              'С каждой его покупки вы будете получать процент на свой баланс!\n\n' \
              f'Ваша реферальная ссылка:  https://t.me/{(await bot.get_me())["username"]}?start={q.from_user.id}\n' \
              f'Ваш процент с покупок реферала: {code_text(str(referral_percent) + "%")}\n\n' \
              f'Вы имеете рефералов: {code_text(referral)} чел.\n' \
              f'Общий заработок с рефералов: {code_text(earning)}₽'
    await bot.send_message(chat_id=q.from_user.id, text=message, reply_markup=keyboard_delete_message())