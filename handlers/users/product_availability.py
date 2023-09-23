from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from loader import dp
from utils.keyboards import *
from database.work_with_sqlite3 import *

@dp.message_handler(Text(contains='Наличие товар'))
async def product_availability(msg: Message):
    message = ""
    for category in all_category():
        category_id = get_id_from_category_name(category)
        message += f'{category}\n'
        for subcategory in all_subcategory(get_id_from_category_name(category)):
            subcategory_id = get_id_from_subcategory_name(subcategory)
            message += f'\t {subcategory} | {int(get_price_subcategory(subcategory_id))}₽/шт. | {get_count_of_items(category_id=category_id, subcategory_id=subcategory_id)}шт.\n'
        message += '\n'
    await msg.answer(message)