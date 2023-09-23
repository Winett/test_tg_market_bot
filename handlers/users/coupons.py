from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.coupon import CreateCoupon
from utils.custom_filters import IsAdmin
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from data.config import time_utc_in_hours


@dp.callback_query_handler(IsAdmin(), Text(contains='create_coupon'))
async def create_coupon_name(q: CallbackQuery, state: FSMContext):
    await CreateCoupon.name_coupon.set()
    await bot.send_message(chat_id=q.from_user.id,
                           text='Введите, пожалуйста, название вашего купона так, как он будет применяться',
                           reply_markup=keyboard_cancel())


@dp.message_handler(state=CreateCoupon.name_coupon)
async def create_coupon_amount(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer(
        'Введите ценность вашего купона, сколько будет зачисляться на баланс пользователю за активацию\n\nНужно отправить просто число',
        reply_markup=keyboard_cancel())
    await CreateCoupon.next()


@dp.message_handler(state=CreateCoupon.amount)
async def create_coupon_expiration_date(msg: Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await msg.answer(
        f'Введите, пожалуйста, срок, сколько будет активен купон\n'
        f'Пример ввода: {code_text("ГОД-МЕСЯЦ-ДЕНЬ ЧАСЫ-МИНУТЫ-СЕКУНДЫ")} или {code_text("2 day")} или {code_text("3 hour")}\n'
        f'Допустим, если вы укажите {bold_text("2 day")}, то купон будет действовать ровно 2 дня, начиная с этого момента!',
        reply_markup=keyboard_cancel())
    await CreateCoupon.next()


@dp.message_handler(state=CreateCoupon.expiration_date)
async def generation_coupon(msg: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name'].upper()
    amount = data['amount']
    expiration_date = msg.text
    add_coupon(coupon_name=name, expiration_date=expiration_date, amount=amount)
    await msg.answer(f'Вы успешно создали купон {code_text(name)} !\n'
                     f'При его вводе пользователь получит {amount}₽\n'
                     f'Купон истекает: {bold_text(get_coupon(name)[0])} по UTC+{time_utc_in_hours}')
    await state.finish()
