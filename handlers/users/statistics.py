from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from utils.markdown import *
from database.work_with_sqlite3 import *
from utils.custom_filters import IsAdmin


@dp.callback_query_handler(Text(equals='statistics'), IsAdmin())
async def statistics(q: CallbackQuery):
    categories = all_category()
    list_of_categories = "\n\t\t".join(categories)
    subcategories = all_subcategory_for_statistics()
    list_of_subcategories = "\n\t\t".join(subcategories)
    activity_users_now = get_activity_users()
    count_today, summ_today = complete_purchase_today()
    count_7, summ_7 = complete_purchase_last_7_day()
    count_14, summ_14 = complete_purchase_last_14_day()
    count_moth, summ_month = complete_purchase_month()
    user_today, amount_today = user_who_made_the_largest_purchase_amount_for_today()
    user_7_day, amount_7_day = user_who_made_the_largest_purchase_amount_for_last_7_day()
    user_14_day, amount_14_day = user_who_made_the_largest_purchase_amount_for_last_14_day()
    user_month, amount_month = user_who_made_the_largest_purchase_amount_for_last_month()
    top_user, top_user_amount = user_who_made_the_largest_purchase_amount()
    message = 'Статистика по боту!\n\n' \
              f'<b>Вы имеете {len(categories)} категорий</b>:\n\t\t' \
              f'{list_of_categories}\n' \
              f'<b>Вы имеете {len(subcategories)} подкатегорий</b>:\n\t\t' \
              f'{list_of_subcategories}\n' \
              f'{bold_text("Всего аккаутов в боте")}: {code_text(count_of_all_accounts())}\n\n' \
              f'<b>Всего пользователь, зарегистрировавшихся в боте</b>: {code_text(count_of_all_users())}\n' \
              f'<b>Активных пользователей сейчас</b>: <code>{activity_users_now}</code>\n\n' \
              f'<b>Совершено покупок за эти сутки: <code>{count_today}</code>, на сумму <code>{summ_today}</code>₽</b>\n' \
              f'<b>Совершено покупок за последние 7 дней: <code>{count_7}</code>, на сумму <code>{summ_7}</code>₽</b>\n' \
              f'<b>Совершено покупок за последние 14 дней: <code>{count_14}</code>, на сумму <code>{summ_14}</code>₽</b>\n' \
              f'<b>Совершено покупок за месяц: <code>{count_moth}</code>, на сумму <code>{summ_month}</code>₽</b>\n\n' \
              f'<b>Пользователь, который сделал наибольшую по сумме покупку за сегодня: @{user_today}, на сумму <code>{amount_today}</code>₽</b>\n' \
              f'<b>Пользователь, который сделал наибольшую по сумме покупку за последние 7 дней: @{user_7_day}, на сумму <code>{amount_7_day}</code>₽</b>\n' \
              f'<b>Пользователь, который сделал наибольшую по сумме покупку за последние 14 дней: @{user_14_day}, на сумму <code>{amount_14_day}</code>₽</b>\n' \
              f'<b>Пользователь, который сделал наибольшую по сумме покупку за последние месяц: @{user_month}, на сумму <code>{amount_month}</code>₽</b>\n\n' \
              f'<b>Всего совершенно покупок в боте</b>: <code>{count_of_purchase()}</code>\n' \
              f'<b>Общая сумма покупок: <code>{total_price_in_purchase_history()}</code>₽</b>\n' \
              f'<b>Топ пользователь по покупкам: @{top_user}, на сумму <code>{top_user_amount}</code>₽</b>'

    await bot.send_message(chat_id=q.from_user.id, text=message)