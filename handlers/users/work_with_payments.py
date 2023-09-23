from os import remove

from aiogram import Bot
from aiogram.types import InputFile

from database.work_with_sqlite3 import *
from data.config import referral_percent, limit_account_to_send_in_message
from utils.yoomoney_method import operation_history
from utils.markdown import *
from utils.keyboards import *


async def send_items_after_buying(bot: Bot, data: dict):
    '''

    :param bot:
    :param data: category_id, subcategory_id, count, total_sum, price_per_item, payment_method, user_id
    :return:
    '''
    category_id = data['category_id']
    subcategory_id = data['subcategory_id']
    count = data['count']
    total_sum = data['total_sum']
    price_per_item = data['price_per_item']
    payment_method = data.get('payment_method')
    user_id = data['user_id']
    ids, accounts = select_accounts(category_id=category_id, subcategory_id=subcategory_id, count=count)
    accounts = list(map(lambda x: x[0:2], accounts))
    accounts = list(map(lambda x: ':'.join(x), accounts))
    refer_id = get_refer_id(user_id)
    if refer_id:
        add_balance_by_referral(refer_id, int(total_sum * (referral_percent / 100)))
    message = f"Ваш заказ успешно оплачен!\n\n"
    item_name = f'{get_name_from_category_id(category_id)} - {get_name_from_subcategory_id(subcategory_id)}'
    add_purchase_history(user_id=user_id, item_name=item_name, count_of_item=count,
                         price_per_item=price_per_item, total_price=total_sum, payment_method=payment_method, category_id=category_id, subcategory_id=subcategory_id)
    if len(accounts) <= limit_account_to_send_in_message:
        for acc in accounts:
            add_to_message = code_text(acc) + '\n'
            message += add_to_message

        await bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard_start())
    else:
        with open(
                f'{user_id}_{get_name_from_category_id(category_id)}_{get_name_from_subcategory_id(subcategory_id)}.txt',
                'w') as f:
            for acc in accounts:
                f.write(acc + '\n')
        await bot.send_document(chat_id=user_id, document=InputFile(
            path_or_bytesio=f'{user_id}_{item_name.replace(" - ", "_")}.txt'), caption=message,
                                reply_markup=keyboard_start())
        remove(f'{user_id}_{item_name.replace(" - ", "_")}.txt')
    delete_accounts(ids)
    if payment_method == 'payment_from_account':
        subtract_balance(user_id=user_id, minus_balance=total_sum)


async def send_balance_after_addition_balance(bot: Bot, data: dict):
    value = data['value']
    user_id = data['user_id']
    add_balance(user_id=user_id, plus_balance=value)
    balance = get_user_balance(user_id=user_id)
    await bot.send_message(chat_id=user_id,
                           text=f'Вы успешно пополнили баланс на сумму {bold_text(value)}₽\n\nВаш текущий баланс: {bold_text(balance)}₽')


async def check_payment_yoomoney(label):
    check = operation_history(label=label)
    if len(check.get('operations', [])) > 0:
        return True
    else:
        return False
