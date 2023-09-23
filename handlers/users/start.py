from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from data.config import admins_id
from loader import dp, bot
from utils.keyboards import *
from database.work_with_sqlite3 import *

@dp.message_handler(commands=['start'], state='*')
async def command_start(msg: Message, state: FSMContext):
    await state.finish()
    if check_user_in_database(msg.from_user.id) is None:
        refer_id = msg.get_args()
        if not bool(refer_id):
            refer_id = None
        else:
            await bot.send_message(chat_id=refer_id, text=f'У вас появился новый реферал @{msg.from_user.username}!')
        add_new_user(user_id=msg.from_user.id, user_name=msg.from_user.username, refer_id=refer_id)

    # if msg.from_user.id in admins_id:
    #     await msg.answer(f"Вас приветствует Админ-панель!", reply_markup=gen_buttons(['Создать купон', 'Выслать человеку баланс', 'Добавить товар/несколько товаров'], row_width=2))
    # else:
    await msg.answer(f"Маркет бот по чему-либо\nВыберите категорию: ", reply_markup=keyboard_start())
    # await msg.answer(f"Маркет бот по чему-либо\nВыберите категорию: ", reply_markup=k)
