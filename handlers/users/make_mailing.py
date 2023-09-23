import asyncio

import aiogram.utils.exceptions

from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.mailing import Mailing
from loader import dp, bot
from utils.markdown import *
from utils.keyboards import *
from database.work_with_sqlite3 import *
from utils.custom_filters import IsAdmin


@dp.callback_query_handler(Text(equals='make_mailing'), IsAdmin(), state='*')
async def start_mailing(q: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=q.from_user.id, text='Введите название рассылки: ')
    await Mailing.wait_name_of_mailing.set()


@dp.message_handler(IsAdmin(), state=Mailing.wait_name_of_mailing)
async def get_name_mailing(msg: Message, state: FSMContext):
    await msg.answer('Назние рассылки успешно добавлено.\nОтправите сообщение, которое должно быть разослано')
    await state.update_data(name_mailing=msg.text)
    await Mailing.next()


# @dp.message_handler(IsAdmin(), is_media_group=True, state=Mailing.wait_message_to_mailing, content_types=[ContentType.ANY])
# async def get_message_to_sending(msg: Message, state: FSMContext):
#     await state.update_data(message_id_to_sending=msg.message_id)
#     await msg.answer('Добавить inline кнопки?', reply_markup=keyboard_use_inline_button_in_mailing())
#     await Mailing.next()

@dp.message_handler(IsAdmin(), state=Mailing.wait_message_to_mailing, content_types=[ContentType.ANY])
async def get_message_to_sending(msg: Message, state: FSMContext):
    await state.update_data(message_id_to_sending=msg.message_id)
    await msg.answer('Добавить inline кнопки?', reply_markup=keyboard_use_inline_button_in_mailing())
    await Mailing.next()


@dp.callback_query_handler(state=Mailing.use_button_for_mailing)
async def button_for_mailing(q: CallbackQuery, state: FSMContext):
    match q.data:
        case "add_button":
            await q.message.edit_text('Отправьте текст для кнопки')
            await state.update_data(message_id_to_edit=q.message.message_id)
            await Mailing.next()
        case "no_button":
            data = await state.get_data()
            await bot.delete_message(chat_id=q.from_user.id, message_id=q.message.message_id)
            await confirm(user_id=q.from_user.id, message_id=data['message_id_to_sending'])
        case _:
            await q.message.edit_text('Произошла ошибка')
            await state.finish()


@dp.message_handler(state=Mailing.wait_message_for_button)
async def name_of_button(msg: Message, state: FSMContext):
    msg_id = (await state.get_data())['message_id_to_edit']
    await state.update_data(button_text=msg.text)
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await bot.edit_message_text(text=f'Отправьте ссылку для кнопки "{msg.text}"', chat_id=msg.from_user.id,
                                message_id=msg_id)
    await Mailing.next()


@dp.message_handler(state=Mailing.wait_url_for_button)
async def url_for_button(msg: Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    # await state.finish()
    keyboard = keyboard_for_mailing(button_text=data['button_text'], button_url=msg.text)
    await state.update_data(keyboard=keyboard)
    await confirm(user_id=msg.from_user.id, message_id=data['message_id_to_sending'],
                  keyboard=keyboard_for_mailing(button_text=data['button_text'], button_url=msg.text))


async def confirm(user_id, message_id, keyboard=None):
    await bot.copy_message(chat_id=user_id, from_chat_id=user_id, message_id=message_id, reply_markup=keyboard)
    await bot.send_message(chat_id=user_id, text='Данное сообщение будет разослано. Подтвердите рассылку',
                           reply_markup=keyboard_confirm_sender())
    await Mailing.pre_message_to_mailing.set()


@dp.callback_query_handler(state=Mailing.pre_message_to_mailing)
async def start_mailing(q: CallbackQuery, state: FSMContext):
    match q.data:
        case 'confirm_mailing':
            data = await state.get_data()
            table_name = data['name_mailing']
            msg_id_to_mailing = data['message_id_to_sending']
            keyboard = data.get('keyboard', None)
            await state.finish()
            # sender = MailingMessage(table_name=table_name)
            await sender_decide(table_name=table_name, message_id_to_mailing=msg_id_to_mailing, user_id_admin=q.from_user.id, keyboard=keyboard)
        case 'cancel_mailing':
            await state.finish()
            await bot.send_message(chat_id=q.from_user.id, text='Рассылка отменена')


async def sender_decide(table_name, message_id_to_mailing, user_id_admin, keyboard=None):
    create_table_for_mailing(table_name=table_name)
    await bot.send_message(chat_id=user_id_admin, text='Начинаю расслыку')
    user_ids = get_all_user_ids_for_mailing(table_name=table_name)
    success_message = 0
    for user_id in user_ids:
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=user_id_admin, message_id=message_id_to_mailing,
                                   reply_markup=keyboard)
            change_status_for_mailing(user_id=user_id, status='success', table_name=table_name)
            success_message += 1
        except aiogram.utils.exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except aiogram.utils.exceptions.BotBlocked:
            change_status_for_mailing(table_name=table_name, user_id=user_id, status='unsuccess',
                                      description='Пользователь заблокировал бота')
        except aiogram.utils.exceptions.ChatNotFound:
            change_status_for_mailing(table_name=table_name, user_id=user_id, status='unsuccess',
                                      description='Чат не найден')
        except Exception as e:
            change_status_for_mailing(table_name=table_name, user_id=user_id, status='unsuccess',
                                      description=f'{e}')
        await asyncio.sleep(.06)
    errors, ids = get_unique_description_error(table_name=table_name)
    errors = f'\n'.join(errors)
    if len(ids) == 0:
        await bot.send_message(chat_id=user_id_admin,
                               text=f'Успешно разослано [{success_message}/{success_message + len(ids)}] сообщений для рассылки {table_name}')
    else:
        # await bot.send_message(chat_id=user_id_admin,
                               # text=f'Успешно разослано [{success_message}/{success_message + len(ids)}] сообщений\nОсновные ошибки, которые произошли при рассылке: \n\n'
                               #      f'{errors}\n\n'
                               #      f'Удалить пользователей, у которых возникла ошибка?',
                               # reply_markup=keyboard_stay_users_after_errors_or_no())
        await bot.send_message(chat_id=user_id_admin,
                               text=f'Успешно разослано [{success_message}/{success_message + len(ids)}] сообщений для рассылки {table_name}\nОсновные ошибки, которые произошли при рассылке: \n\n'
                                    f'{errors}')
    delete_mailing_table(table_name=table_name)

# @dp.callback_query_handler(Text(endswith='users_with_errors_mailing'), state='*')
# async def work_with_user_with_errors_mailing(q: CallbackQuery, state: FSMContext):
#     match q.data:
#         case 'delete_users_with_errors_mailing':
#             # ids = (await state.get_data())['ids']
#             # delete_accounts(account_ids=ids)
#             ...
#         case 'stay_users_with_errors_mailing':
#             return
#     await state.finish()


# class MailingMessage:
#
#     def __init__(self, table_name):
#         self.table_name = table_name
#
#     async def sender_decide(self, message_id_to_mailing, user_id_admin, keyboard=None):
#         await bot.send_message(chat_id=user_id_admin, text='Начинаю расслыку')
#         user_ids = get_all_user_ids_for_mailing(table_name=self.table_name)
#         success_message = 0
#         for user_id in user_ids:
#             try:
#                 await bot.copy_message(chat_id=user_id, from_chat_id=user_id_admin, message_id=message_id_to_mailing,
#                                        reply_markup=keyboard)
#                 change_status_for_mailing(user_id=user_id, status='success', table_name=self.table_name)
#                 success_message += 1
#             except aiogram.utils.exceptions.RetryAfter as e:
#                 await asyncio.sleep(e.timeout)
#             except aiogram.utils.exceptions.BotBlocked:
#                 change_status_for_mailing(table_name=self.table_name, user_id=user_id, status='unsuccess',
#                                           description='Пользователь заблокировал бота')
#             except aiogram.utils.exceptions.ChatNotFound:
#                 change_status_for_mailing(table_name=self.table_name, user_id=user_id, status='unsuccess',
#                                           description='Чат не найден')
#             except Exception as e:
#                 change_status_for_mailing(table_name=self.table_name, user_id=user_id, status='unsuccess',
#                                           description=f'{e}')
#             await asyncio.sleep(.06)
#         errors, ids = get_unique_description_error(table_name=self.table_name)
#         errors = f'\n'.join(errors) if errors[0] is not None else ''
#         if len(ids) == 0:
#             await bot.send_message(chat_id=user_id_admin,
#                                    text=f'Успешно разослано [{success_message}/{success_message + len(ids)}] сообщений')
#         else:
#             await bot.send_message(chat_id=user_id_admin,
#                                    text=f'Успешно разослано [{success_message}/{success_message + len(ids)}] сообщений\nОсновные ошибки, которые произошли при рассылке: \n\n'
#                                         f'{errors}\n\n'
#                                         f'Удалить пользователей, у которых возникла ошибка?',
#                                    reply_markup=keyboard_stay_users_after_errors_or_no())
#
#     @staticmethod
#     @dp.callback_query_handler(Text(endswith='users_with_errors_mailing'), state='*')
#     async def work_with_user_with_errors_mailing(q: CallbackQuery, state: FSMContext):
#         match q.data:
#             case 'delete_users_with_errors_mailing':
#                 # ids = (await state.get_data())['ids']
#                 # delete_accounts(account_ids=ids)
#                 ...
#             case 'stay_users_with_errors_mailing':
#                 return
#         await state.finish()
