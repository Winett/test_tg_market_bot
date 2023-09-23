from datetime import datetime

BOT_TOKEN = '1675511108:AAFtERRH-qkiKucENNVeKpN7-tBvqS2osLY'
time_utc_in_hours = (datetime.now() - datetime.utcnow()).seconds // 60 // 60
admins_id = [625839825]
db = 'sqlite3'
name_of_db = 'test.db'
__folder_for_db__ = 'data'
client_id = '4BB1533399A9FC1046226F6D69F5F2CD4423127E60F11FBD0E5B96DA77E268E2'
yoomoney_token = '4100117890101609.3D8AE74B01CB9AC7437E2BB82A531C3A936AAD92A04CC4ACB17F4770170F73EB048A3F581F760BD510C032D1ABB987431B00F932E06D4A26004FE82A94CD5B4D445DE423B2843E15ECE3C8D3E55900A299433E92FA8BDEAB4BD86DD5385F8EF1A164B3E3BFF652094C353A90FB116BB951F203D00C1CC6CDE8B24B134E227AEF'
transfer_yoomoney_fee = 3 #Комиссия ЮMoney в процентах
referral_percent = 10 #Процент от покупок реферала рефероводу
limit_account_to_send_in_message = 2 #Если пользователь покупает 10 аккаутов или меньше, то данные высылаются ему сообщением, если больше, то txt файлом

CLIENT_ID_LOLZ = '65w0q5vxhg'
CLIENT_SECRET_LOLZ = '9w0vexpin8glkor'
TOKEN_LOLZ = '057e7d2726f28894e09219de9ed87bcc1521974d'
USER_NAME_LOLZ = 'Winet'

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