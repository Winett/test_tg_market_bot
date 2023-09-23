from datetime import datetime

BOT_TOKEN = ''
time_utc_in_hours = (datetime.now() - datetime.utcnow()).seconds // 60 // 60
admins_id = []
db = 'sqlite3'
name_of_db = 'test.db'
__folder_for_db__ = 'data'
client_id = ''
yoomoney_token = ''
transfer_yoomoney_fee = 3 #Комиссия ЮMoney в процентах
referral_percent = 10 #Процент от покупок реферала рефероводу
limit_account_to_send_in_message = 2 #Если пользователь покупает 10 аккаутов или меньше, то данные высылаются ему сообщением, если больше, то txt файлом

TIME_TO_WAIT_PAYMENT_IN_SECONDS = 300


for_user_history = {
    'payment_from_account': 'С баланса аккаунта',
    'yoomoney_method': 'ЮMoney | Банковская карта',
    # 'lolz_method': 'Lolz'
}
keyboard_for_profile = [
            'Покупки', 'buys',
            'Активировать промокод', 'activate_coupon',
            'Пополнить баланс', 'add_balance',
            'История пополнений', 'history_add_balance',
            'Реферальная система', 'referral_system'
]
keyboard_for_profile_admin = [
    'Создать купон', 'create_coupon',
    'Изменение категорий', 'add_edit_category',
    'Изменение подкатегорий', 'add_edit_subcategory',
    'Добавить товар', 'add_items',
    'Сделать рассылку', 'make_mailing',
    'Статистика', 'statistics'
]
payment_methods = [
    'С баланса аккаунта', "payment_from_account",
    f"ЮMoney | Банковская карта | Комиссия {transfer_yoomoney_fee}%", "yoomoney_method",
    # 'Lolz', 'lolz_method'
]
