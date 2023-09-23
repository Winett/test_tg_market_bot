from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.activation_coupon import ActivateCoupon
from utils.custom_filters import IsAdmin
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *


@dp.callback_query_handler(Text(contains='activate_coupon'))
async def activate_coupon(q: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=q.from_user.id, text='🎁 Введите, пожалуйста, купон')
    await ActivateCoupon.wait_coupon.set()


@dp.message_handler(state=ActivateCoupon.wait_coupon)
async def activation_coupon(msg: Message, state: FSMContext):
    coupon_name = msg.text.upper()
    date, amount = get_coupon(coupon_name=coupon_name)
    await state.finish()
    if date is None:
        await msg.answer('Извините, купон не найдет, или срок действия его истёк', reply_markup=keyboard_start())
    else:
        status_code_for_user = user_used_coupon(coupon_name=coupon_name, user_id=msg.from_user.id)
        if status_code_for_user:
            await msg.answer('Вы уже активировали этот купон!')
            return
        change_status_coupon(coupon_name=coupon_name, user_id=msg.from_user.id)
        add_balance(user_id=msg.from_user.id, plus_balance=amount)
        await msg.answer(f'Вы успешно применили купон {code_text(coupon_name)}! Вам зачисленно на баланс {bold_text(f"{amount}₽")}', reply_markup=keyboard_start())