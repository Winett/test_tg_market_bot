from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from database.work_with_sqlite3 import all_subcategory, all_category
from data.config import transfer_yoomoney_fee, keyboard_for_profile, keyboard_for_profile_admin, payment_methods


def keyboard_start(row_width: int = 2) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    data = ['Купить товар', 'Наличие товаров', 'Профиль']
    buttons = []
    for button in data:
        buttons.append(KeyboardButton(button))
    keyboard.add(*buttons)
    return keyboard


def keyboard_history_buys(data: list, row_width: int = 1):  # purchase_id, item_name, count_of_account
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    buttons = []
    for info in data:
        purchase_id, item_name, count_of_account = info
        buttons.append(InlineKeyboardButton(text=f'{item_name} | {count_of_account} шт.',
                                            callback_data=f'history_buys {purchase_id}'))
    keyboard.add(*buttons)
    return keyboard


def keyboard_profile(row_width: int = 2) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = keyboard_for_profile
    keys = []
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*keys)
    return keyboard


def keyboard_profile_admins(row_width: int = 2) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = keyboard_for_profile
    admin_data = keyboard_for_profile_admin
    keys = []
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*keys)
    keyboard.row(InlineKeyboardButton(text='⚙ Админ панель ⚙', callback_data=' '))
    keys = []
    for ind in range(0, len(admin_data), 2):
        name_button, callback_data = admin_data[ind], admin_data[ind + 1]
        keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*keys)
    return keyboard


def keyboard_yoomoney_method(url, row_width: int = 1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = ['Я оплатил(-а)', "check_payment_yoomoney", '❌ Отмена операции', 'cancel']
    buttons = []
    keyboard.row(InlineKeyboardButton('Оплатить', url=url))
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        buttons.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*buttons)
    return keyboard


def keyboard_cancel(row_width: int = 1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = ['❌ Отмена', 'cancel']
    buttons = []
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        buttons.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*buttons)
    return keyboard


def keyboard_delete_message(row_width: int = 1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = ['❌Удалить сообщение❌', 'delete_message']
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keyboard.add(InlineKeyboardButton(name_button, callback_data=callback_data))
    return keyboard


def keyboard_for_callback_subcategory(max_keyboard_button, row_width=5):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    buttons = []
    for button in range(1, max_keyboard_button):
        name_button, callback_data = button, f'buy {button}'
        buttons.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*buttons)
    keyboard.row(InlineKeyboardButton('Назад', callback_data="back_to_subcategory"),
                 InlineKeyboardButton('Главная', callback_data="Главная"))
    return keyboard


def keyboard_for_callback_category(category_id, row_width: int = 2):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = all_subcategory(category_id=category_id)
    buttons = []
    for button in data:
        name_button, callback_data = button, f'subcategory {button}'
        buttons.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton('Назад', callback_data="back_to_category"),
                 InlineKeyboardButton('Главная', callback_data="Главная"))
    return keyboard


def keyboard_for_buy_item(row_width: int = 2):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = all_category()
    buttons = []
    for button in data:
        name_button, callback_data = button, f'category {button}'
        buttons.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    keyboard.add(*buttons)
    keyboard.row(InlineKeyboardButton('Главная', callback_data="Главная"))
    return keyboard


def keyboard_for_payment(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = payment_methods + ['❌ Отмена', 'cancel']
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keyboard.add(InlineKeyboardButton(name_button, callback_data=callback_data))
    return keyboard


def keyboard_for_add_balance(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = payment_methods[2:] + ['❌ Отмена', 'cancel']
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keyboard.add(InlineKeyboardButton(name_button, callback_data=callback_data))
    return keyboard


def keyboard_type_of_adding_data(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = [
        'login:password', 'type_of_data login:password',
        'access_token', 'type_of_data access_token',
        'login:password:access_token', 'type_of_data login:password:access_token'
    ]
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keyboard.add(InlineKeyboardButton(name_button, callback_data=callback_data))
    return keyboard


def keyboard_work_with_category(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = [
        'Изменить категорию', 'edit_category',
        'Создать новую категорию', 'add_category',
    ]
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keyboard.add(InlineKeyboardButton(name_button, callback_data=callback_data))
    return keyboard


def keyboard_confirm_buying_from_user_balance(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    data = [
               'Подтвердить покупку', 'confirm_buying_from_user_balance'
           ] + ['❌ Отмена', 'cancel']
    for ind in range(0, len(data), 2):
        name_button, callback_data = data[ind], data[ind + 1]
        keyboard.add(InlineKeyboardButton(name_button, callback_data=callback_data))
    return keyboard


def keyboard_use_inline_button_in_mailing(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    keyboard.add(InlineKeyboardButton(text='Да', callback_data='add_button'),
                 InlineKeyboardButton('Нет', callback_data='no_button'))
    return keyboard


def keyboard_confirm_sender(row_width: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    keyboard.add(InlineKeyboardButton(text='Подтвердить рассылку', callback_data='confirm_mailing'), InlineKeyboardButton(text='Отменить рассылку', callback_data='cancel_mailing'))
    return keyboard


def keyboard_for_mailing(button_text, button_url, row_width=1):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    keyboard.add(InlineKeyboardButton(text=button_text, url=button_url))
    return keyboard


def keyboard_stay_users_after_errors_or_no(row_width: int = 2):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data='delete_users_with_errors_mailing'), InlineKeyboardButton('Оставить', callback_data='stay_users_with_errors_mailing'))
    return keyboard


# def gen_inline_buttons(list_of_name_buttons: list,
#                        use_as_callback_data_next_value_from_list=False,
#                        row_width: int = 1,
#                        post_script: str | None = None,
#                        first_button: str | list | None = None,
#                        add_first_buttons_as_row: bool = False,
#                        use_as_callback_data_next_value_for_first_button=False,
#                        row_width_for_first_buttons: int = 1,
#                        last_button: str | list | None = None,
#                        add_last_buttons_as_row: bool = False,
#                        row_width_for_last_buttons: int = 1,
#                        use_as_callback_data_next_value_for_last_button: bool = False,
#                        use_in_callback_data_name_of_button: bool = False) -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardMarkup(row_width=row_width)
#
#     if first_button is not None:
#         if isinstance(first_button, str):
#                 keyboard.row(InlineKeyboardButton(first_button, callback_data=first_button))
#         elif isinstance(first_button, list):
#             keys = []
#             if use_as_callback_data_next_value_for_first_button:
#                 for ind in range(0, len(first_button), 2):
#                     name_button, callback_data = first_button[ind], first_button[ind + 1]
#                     keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
#             else:
#                 for key in first_button:
#                     keys.append(InlineKeyboardButton(key, callback_data=f'{post_script} {key}'))
#
#             if add_first_buttons_as_row:
#                 keyboard.row(*keys)
#             else:
#                 keyboard.add(*keys)
#
#     if use_as_callback_data_next_value_from_list:
#         keys = []
#         for ind in range(0, len(list_of_name_buttons), 2):
#             name_button, callback_data = list_of_name_buttons[ind], list_of_name_buttons[ind + 1]
#             keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
#     else:
#         keys = [InlineKeyboardButton(name_button,
#                                      callback_data=f'{post_script} {name_button * use_in_callback_data_name_of_button}')
#                 for name_button in list_of_name_buttons]
#     keyboard.add(*keys)
#
#     if last_button is not None:
#         if isinstance(last_button, str):
#             button = InlineKeyboardButton(last_button, callback_data=last_button)
#
#             if add_last_buttons_as_row:
#                 keyboard.row(button)
#             else:
#                 keyboard.add(button)
#         elif isinstance(last_button, list):
#             keys = []
#             if use_as_callback_data_next_value_for_last_button:
#                 for ind in range(0, len(last_button), 2):
#                     name_button, callback_data = last_button[ind], last_button[ind + 1]
#                     keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
#             else:
#                 for key in last_button:
#                     keys.append(InlineKeyboardButton(key, callback_data=f'{post_script} {key}'))
#
#             if add_last_buttons_as_row:
#                 keyboard.row(*keys)
#             else:
#                 keyboard.add(*keys)
#
#     return keyboard
#
# def gen_inline_buttons(list_of_name_buttons: list,
#                        use_as_callback_data_next_value_from_list=False,
#                        row_width: int = 1,
#                        post_script: str | None = None,
#                        first_button: str | list | None = None,
#                        add_first_buttons_as_row: bool = False, #если False, то для кнопок будет срабатывать метод add
#                        use_as_callback_data_next_value_for_first_button=False,
#                        row_width_for_first_buttons: int = 1,
#                        last_button: str | list | None = None,
#                        add_last_buttons_as_row: bool = False,
#                        row_width_for_last_buttons: int = 1,
#                        use_as_callback_data_next_value_for_last_button: bool = False,
#                        use_in_callback_data_name_of_button: bool = False) -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardMarkup(row_width=row_width)
#     # if isinstance(first_button, str):
#     #     keyboard.row(InlineKeyboardButton())
#
#
def gen_inline_buttons(list_of_name_buttons: list,
                       use_as_callback_data_next_value_from_list=False,
                       row_width: int = 1,
                       post_script: str | None = None,
                       first_button: str | None = None,
                       last_button: str | list | None = None,
                       use_as_callback_data_next_value_for_first_button=False,
                       use_as_callback_data_next_value_for_last_button=False,
                       row_width_for_last_button: int = 1,
                       # callback_data_for_last_button=None,
                       use_in_callback_data_name_of_button=True) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    if first_button is not None:
        keyboard.row(InlineKeyboardButton(first_button, callback_data=first_button))
    if use_as_callback_data_next_value_from_list:
        keys = []
        for ind in range(0, len(list_of_name_buttons), 2):
            name_button, callback_data = list_of_name_buttons[ind], list_of_name_buttons[ind + 1]
            keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
    else:
        keys = [InlineKeyboardButton(name_button,
                                     callback_data=f'{post_script} {name_button * use_in_callback_data_name_of_button}')
                for name_button in list_of_name_buttons]
    keyboard.add(*keys)
    if isinstance(last_button, str):
        keyboard.row(InlineKeyboardButton(last_button, callback_data=last_button))
    elif isinstance(last_button, list):
        keys = []
        if use_as_callback_data_next_value_for_last_button:
            for ind in range(0, len(last_button), 2):
                name_button, callback_data = last_button[ind], last_button[ind + 1]
                keys.append(InlineKeyboardButton(name_button, callback_data=callback_data))
        else:
            for key in last_button:
                keys.append(InlineKeyboardButton(key, callback_data=f'{post_script} {key}'))
        keyboard.row(*keys)
    return keyboard
#
#
# def gen_buttons(list_of_name_buttons: list, row_width: int = 1, first_button: str | None = None,
#                 last_button: str | list | None = None) -> ReplyKeyboardMarkup:
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
#     if first_button is not None:
#         keyboard.row(KeyboardButton(first_button))
#     keys = [InlineKeyboardButton(name_button) for name_button in list_of_name_buttons]
#     keyboard.add(*keys)
#     if last_button is not None:
#         keyboard.row(KeyboardButton(last_button))
#     return keyboard
