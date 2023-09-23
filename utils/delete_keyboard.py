from aiogram import types
from loader import dp

@dp.message_handler(commands='delete_keyboard', state='*')
async def delete_keyboard(msg: types.Message):
    await msg.answer('Клавиатура успешно удалена!', reply_markup=types.ReplyKeyboardRemove())