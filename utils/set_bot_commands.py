from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'), # пока добавляем только одну команду
            types.BotCommand('delete_keyboard', 'Удалить клавиатуру')
            # types.BotCommand('add_channel', 'Добавить канал'),
            # types.BotCommand('add_post', 'Добавить пост')
        ]
    )
