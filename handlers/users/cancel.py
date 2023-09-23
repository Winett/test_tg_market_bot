from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from utils.keyboards import *
from data.config import *



@dp.callback_query_handler(Text(equals='cancel'), state='*')
async def cancel(q: CallbackQuery, state=FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=q.message.chat.id, message_id=q.message.message_id)
    # if q.from_user.id in admins_id:
    #     await bot.send_message(chat_id=q.message.chat.id, text="Вас приветствует Админ-панель!", reply_markup=gen_buttons(['Создать купон', 'Выслать человеку баланс', 'Добавить товар/несколько товаров'], row_width=2))
    # else:
    await bot.send_message(chat_id=q.message.chat.id, text=f"Маркет бот по чему-либо\nВыберите категорию: ",
                         reply_markup=keyboard_start())