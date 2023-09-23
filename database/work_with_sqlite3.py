import sqlite3
from datetime import datetime
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from loader import scheduler_bg

from data.config import name_of_db, __folder_for_db__, time_utc_in_hours

scheduler_bg = BackgroundScheduler()
scheduler_io = AsyncIOScheduler()

def create_db(name_db: str, path: str) -> None:
    path = f'..\\{path}\\{name_db}' if __name__ == '__main__' else f'{path}\\{name_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    '''SELECT category.name as category_name, subcategory.name as subcategory_name, 
subcategory.price, subcategory.description, accounts.login, accounts.password
FROM accounts JOIN category ON accounts.category_id = category.id JOIN subcategory ON accounts.subcategory_id = subcategory.id
'''
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users'
        '('
        'user_id INT,'
        'user_name VARCHAR(255),'
        'registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
        'last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
        'balance INT DEFAULT(0),'
        'role VARCHAR DEFAULT "member",'
        'refer_id INT,'
        'earning_from_referral REAL DEFAULT(0)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS category'
        '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name VARCHAR(30)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS subcategory'
        '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'category_id INT,'
        'name VARCHAR(30),'
        'price REAL,'
        'description VARCHAR,'
        'FOREIGN KEY (category_id) REFERENCES category(id)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS accounts('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'category_id INT,'
        'subcategory_id INT,'
        'login VARCHAR,'
        'password VARCHAR,'
        'access_token VARCHAR(255),'
        'FOREIGN KEY (category_id) REFERENCES category(id),'
        'FOREIGN KEY (subcategory_id) REFERENCES subcategory(id)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS coupons('
        'name PRIMARY KEY,'
        'expiration_date datetime,'
        'amount INT'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS purchase_history('
        'purchase_id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'user_id INT,'
        'category_id INT,'
        'subcategory_id INT'
        'item_name VARCHAR,'
        'count_of_item INT,'
        'price_per_item REAL,'
        'total_price REAL,'
        'payment_method VARCHAR,'
        'timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        # 'FOREIGN KEY (user_id) REFERENCES users(user_id)'
        ')')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS payment_history('
        'payment_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'user_id INT,'
        'amount INT,'
        'payment_method VARCHAR,'
        'payment_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
        'status VARCHAR,'
        'label VARCHAR'
        ')')


def add_column_to_db(table_name, column_name, column_type) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'''
    ALTER TABLE {table_name} ADD {column_name} {column_type}
    ''')


def drop_column_to_db(table_name, column_name, *args) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'''
    ALTER TABLE {table_name} DROP COLUMN {column_name}
    ''')


def add_new_user(user_id: int, user_name: str, refer_id: str | int = None) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'INSERT INTO users(registration_date, user_id, user_name, refer_id) VALUES (CURRENT_TIMESTAMP, ?, ?, ?)',
        (user_id, user_name, refer_id))
    con.commit()
    cur.close()
    con.close()


def change_user_role(user_id, new_role):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'UPDATE users SET role = ? WHERE user_id = ?',
        (new_role, user_id,))
    con.commit()


def check_user_in_database(user_id: str | int) -> tuple | None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user = cur.execute(f'''SELECT * FROM users WHERE user_id={user_id}''').fetchone()
    return user


def update_user_last_activity(user_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE user_id = ?', (user_id,))
    con.commit()


def update_username(user_id, user_name):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('UPDATE users SET user_name = ? WHERE user_id = ?', (user_name, user_id,))
    con.commit()


def get_activity_users():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    users = \
        cur.execute('SELECT COUNT(user_id) FROM users WHERE last_activity >= DATETIME("now", "-3 minute")').fetchone()[
            0]
    return users


def count_of_all_users() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur.execute('SELECT COUNT(*) FROM users').fetchone()[0]


def add_category(name) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'INSERT INTO category(name) VALUES (?);',
        (name,)
    )
    con.commit()


def all_category() -> list:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    categories = cur.execute(
        'SELECT name FROM category'
    )
    return list(map(lambda x: x[0], categories.fetchall()))


def get_id_from_category_name(name: str) -> int:
    # print(name)
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    category = cur.execute(
        'SELECT id FROM category WHERE name = ?', (name,)
    ).fetchone()
    return category[0]


def get_name_from_category_id(id: str) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    category = cur.execute(
        'SELECT name FROM category WHERE id = ?', (id,)
    ).fetchone()
    return category[0]


def add_subcategory(name, category_id) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'INSERT INTO subcategory(name, category_id) VALUES (?, ?);',
        (name, category_id,)
    )
    con.commit()


def all_subcategory(category_id) -> list:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    categories = cur.execute(
        'SELECT name FROM subcategory WHERE category_id = ?',
        (category_id,)
    )
    return list(map(lambda x: x[0], categories.fetchall()))


def all_subcategory_for_statistics() -> list:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    categories = cur.execute(
        'SELECT name FROM subcategory',
    )
    return list(map(lambda x: x[0], categories.fetchall()))


def get_id_from_subcategory_name(name: str) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    category = cur.execute(
        'SELECT id FROM subcategory WHERE name = ?', (name,)
    ).fetchone()
    return category[0]


def get_name_from_subcategory_id(id: str) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    category = cur.execute(
        'SELECT name FROM subcategory WHERE id = ?', (id,)
    ).fetchone()
    return category[0]


def get_description_subcategory(subcategory_id) -> str:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    describe = cur.execute('SELECT description FROM subcategory WHERE id = ?', (subcategory_id,)).fetchone()
    return describe[0]


def get_price_subcategory(subcategory_id) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    price = cur.execute('SELECT price FROM subcategory WHERE id = ?', (subcategory_id,)).fetchone()
    return price[0]


def change_name_category(new_name, id) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'UPDATE category SET name = ? WHERE id = ?', (new_name, id)
    )
    con.commit()


def change_name_subcategory(new_name, id) -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'UPDATE subcategory SET name = ? WHERE id = ?', (new_name, id)
    )
    con.commit()


def add_account(category_id, subcategory_id, login=None, password=None, access_token=None,
                type='login:password') -> None:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    if type == 'login:password':
        cur.execute(
            'INSERT INTO accounts(category_id, subcategory_id, login, password) VALUES (?, ?, ?, ?)',
            (category_id, subcategory_id, login, password,)
        )
    elif type == 'access_token':
        cur.execute(
            'INSERT INTO accounts(category_id, subcategory_id, access_token) VALUES (?, ?, ?)',
            (category_id, subcategory_id, access_token,)
        )
    else:
        cur.execute(
            'INSERT INTO accounts(category_id, subcategory_id, login, password, access_token) VALUES (?, ?, ?, ?, ?)',
            (category_id, subcategory_id, login, password, access_token,))
    con.commit()


def add_many_accounts(data: list, type='login:password') -> None:
    '''
    :param data: Должен содержать в себе следущее: data = [(category_id, subcategory_id, login, password, access_token), ...],
    если comment и access_token нет, то автоматически впишутся значения None
    :return:
    '''
    for i in range(len(data)):
        data[i] = tuple(list(data[i]))
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    if type == 'login:password':
        cur.executemany(
            'INSERT INTO accounts(category_id, subcategory_id, login, password) VALUES (?, ?, ?, ?)',
            tuple(data)
        )
    elif type == 'access_token':
        cur.executemany(
            'INSERT INTO accounts(category_id, subcategory_id, access_token) VALUES (?, ?, ?)',
            tuple(data)
        )
    else:
        cur.executemany(
            'INSERT INTO accounts(category_id, subcategory_id, login, password, access_token) VALUES (?, ?, ?, ?, ?)',
            tuple(data))
    con.commit()
    # for i in range(len(data)):
    #     if len(data[i]) < LEN_OF_COLUMN_IN_ACCOUNTS:
    #         data[i] = tuple(list(data[i]) + [None] * (LEN_OF_COLUMN_IN_ACCOUNTS - len(data[i])))
    # path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    # con = sqlite3.connect(path)
    # cur = con.cursor()
    # cur.executemany(
    #     'INSERT INTO accounts(category_id, subcategory_id, login, password, access_token) VALUES (?, ?, ?, ?, ?)',
    #     data
    # )
    con.commit()


def count_of_all_accounts() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur.execute('SELECT COUNT(id) FROM accounts').fetchone()[0]


def count_account_of_category_and_subcategory(category_id: int, subcategory_id: int) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    count = cur.execute('SELECT COUNT(*) FROM accounts WHERE category_id = ? AND subcategory_id = ?',
                        (category_id, subcategory_id,))
    return count.fetchone()[0]


def get_user_balance(user_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    balance = cur.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return balance[0]


def get_count_of_items(category_id, subcategory_id) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    count = cur.execute('SELECT COUNT(*) FROM accounts WHERE category_id = ? AND subcategory_id = ?',
                        (category_id, subcategory_id,)).fetchone()
    return count[0]


def select_accounts(category_id, subcategory_id, count) -> tuple:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    accounts = cur.execute(
        'SELECT id, login, password, access_token FROM accounts WHERE category_id = ? AND subcategory_id = ? LIMIT ?',
        (category_id, subcategory_id, count,)).fetchall()
    accounts = list(map(lambda x: list(x), accounts))
    ids = list(map(lambda x: x.pop(0), accounts))
    return ids, accounts


def delete_accounts(account_ids: list | tuple) -> None:
    # print(tuple(account_ids))
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    # cur.executemany('DELETE FROM accounts WHERE id = ?', tuple(account_ids))
    for account in account_ids:
        cur.execute('DELETE FROM accounts WHERE id = ?', (account,))
    con.commit()


def subtract_balance(user_id, minus_balance):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    balance = get_user_balance(user_id)
    cur.execute('UPDATE users SET balance = ? WHERE user_id = ?', (balance - minus_balance, user_id,))
    con.commit()


def add_balance(user_id, plus_balance):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    balance = get_user_balance(user_id)
    cur.execute('UPDATE users SET balance = ? WHERE user_id = ?', (balance + plus_balance, user_id,))
    con.commit()


def delete_coupon(coupon_name):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('DELETE FROM coupons WHERE name = ?', (coupon_name,))
    cur.execute(f'ALTER TABLE users DROP COLUMN coupon_{coupon_name}')
    con.commit()


def change_status_coupon(coupon_name, user_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'UPDATE users SET coupon_{coupon_name} = ? WHERE user_id = ?', (True, user_id,))
    con.commit()


def user_used_coupon(coupon_name, user_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    status = cur.execute(f'SELECT coupon_{coupon_name} FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return status[0]


def get_coupon(coupon_name):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    try:
        date = cur.execute('SELECT expiration_date, amount FROM coupons WHERE name = ?', (coupon_name,)).fetchone()
        amount = date[1]
        date = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S') + timedelta(hours=time_utc_in_hours)
        if date < datetime.now():
            delete_coupon(coupon_name=coupon_name)
            return None, None
        return date, amount
    except TypeError:  # записи не найдено, купона нет
        return None, None


def add_coupon(coupon_name: str, expiration_date: str, amount: int):
    coupon_name = coupon_name.upper()
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    try:
        expiration_date = datetime.fromisoformat(expiration_date)
        cur.execute(
            'INSERT INTO coupons(name, expiration_date, amount) VALUES (?, ?, ?) ON CONFLICT(name) DO UPDATE SET expiration_date=?, amount=?',
            (coupon_name, expiration_date - timedelta(hours=time_utc_in_hours), amount,
             expiration_date - timedelta(hours=time_utc_in_hours), amount,))
    except ValueError:  # В случаем, если формат даты записан не год-месяц-день и тд, а 2 day
        cur.execute(
            f'INSERT INTO coupons(name, expiration_date, amount) VALUES (?, datetime("now", "+{expiration_date}"), ?) ON CONFLICT(name) DO UPDATE SET expiration_date=datetime("now", "+{expiration_date}"), amount=?',
            (coupon_name, amount, amount,))
    if cur.execute('SELECT expiration_date FROM coupons WHERE name = ?', (coupon_name,)).fetchone()[0] is None:
        cur.execute('DELETE FROM coupons WHERE name = ?', (coupon_name,))
    else:
        cur.execute(f'ALTER TABLE users ADD COLUMN coupon_{coupon_name} BOOLEAN DEFAULT 0')
    con.commit()


def add_purchase_history(user_id, item_name, count_of_item, price_per_item, total_price, payment_method, category_id,
                         subcategory_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        'INSERT INTO purchase_history(user_id, item_name, count_of_item, price_per_item, total_price, payment_method, category_id, subcategory_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (user_id, item_name, count_of_item, price_per_item, total_price, payment_method, category_id, subcategory_id,))
    con.commit()


def check_purchase_history(purchase_id) -> list:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    history = cur.execute('SELECT * FROM purchase_history WHERE purchase_id = ?', (purchase_id,)).fetchone()
    return history


def get_purchase_history_for_buttons(user_id) -> list:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    history = cur.execute('SELECT purchase_id, item_name, count_of_item FROM purchase_history WHERE user_id = ?',
                          (user_id,)).fetchall()
    return history


def delete_purchase_history(ids_history):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    for id in ids_history:
        cur.execute('DELETE FROM purchase_history WHERE purchase_id = ?', (id,))
    con.commit()


def count_of_purchase() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur.execute('SELECT COUNT(purchase_id) FROM purchase_history').fetchone()[0]


def total_price_in_purchase_history():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur.execute('SELECT SUM(total_price) FROM purchase_history').fetchone()[0]


def complete_purchase_today() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    purchase = cur.execute(
        'SELECT COUNT(total_price), SUM(total_price) FROM purchase_history WHERE timestamp >= DATE("now")').fetchone()
    if purchase is None:
        return 0
    return purchase


def complete_purchase_last_7_day() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    purchase = cur.execute(
        'SELECT COUNT(total_price), SUM(total_price) FROM purchase_history WHERE timestamp >= DATE("now", "-6 day")').fetchone()
    if purchase is None:
        return 0
    return purchase


def complete_purchase_last_14_day() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    purchase = cur.execute(
        'SELECT COUNT(total_price), SUM(total_price) FROM purchase_history WHERE timestamp >= DATE("now", "-13 day")').fetchone()
    if purchase is None:
        return 0
    return purchase


def complete_purchase_month() -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    purchase = cur.execute(
        'SELECT COUNT(total_price), SUM(total_price) FROM purchase_history WHERE timestamp >= DATE("now", "-1 month")').fetchone()
    if purchase is None:
        return 0
    return purchase


def user_who_made_the_largest_purchase_amount_for_today():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute('SELECT user_id FROM purchase_history WHERE timestamp >= date("now") GROUP BY user_id ORDER BY SUM(total_price) DESC LIMIT 1').fetchone()
    if user_id is None:
        return 0, 0
    user_id = user_id[0]
    user_name = cur.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    amount = cur.execute('SELECT SUM(total_price) FROM purchase_history WHERE timestamp >= date("now") AND user_id = ?',
                         (user_id,)).fetchone()[0]
    return user_name, amount


def user_who_made_the_largest_purchase_amount_for_last_7_day():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute(
        'SELECT user_id FROM purchase_history WHERE timestamp >= date("now", "-6 day") GROUP BY user_id ORDER BY SUM(total_price) DESC LIMIT 1').fetchone()[
        0]
    user_name = cur.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    amount = cur.execute(
        'SELECT SUM(total_price) FROM purchase_history WHERE timestamp >= date("now", "-6 day") AND user_id = ?',
        (user_id,)).fetchone()[0]
    return user_name, amount


def user_who_made_the_largest_purchase_amount_for_last_14_day():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute(
        'SELECT user_id FROM purchase_history WHERE timestamp >= date("now", "-13 day") GROUP BY user_id ORDER BY SUM(total_price) DESC LIMIT 1').fetchone()[
        0]
    user_name = cur.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    amount = cur.execute(
        'SELECT SUM(total_price) FROM purchase_history WHERE timestamp >= date("now", "-13 day") AND user_id = ?',
        (user_id,)).fetchone()[0]
    return user_name, amount


def user_who_made_the_largest_purchase_amount_for_last_month():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute(
        'SELECT user_id FROM purchase_history WHERE timestamp >= date("now", "-1 month") GROUP BY user_id ORDER BY SUM(total_price) DESC LIMIT 1').fetchone()[
        0]
    user_name = cur.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    amount = cur.execute(
        'SELECT SUM(total_price) FROM purchase_history WHERE timestamp >= date("now", "-1 month") AND user_id = ?',
        (user_id,)).fetchone()[0]
    return user_name, amount


def user_who_made_the_largest_purchase_amount():
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_id = cur.execute(
        'SELECT user_id FROM purchase_history GROUP BY user_id ORDER BY SUM(total_price) DESC LIMIT 1').fetchone()[
        0]
    user_name = cur.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    amount = cur.execute('SELECT SUM(total_price) FROM purchase_history WHERE user_id = ?',
                         (user_id,)).fetchone()[0]
    return user_name, amount


def get_referrals_and_earning(referral_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    referrals = cur.execute(f'SELECT COUNT(*) FROM users WHERE refer_id = ?', (referral_id,)).fetchone()[0]
    earning = cur.execute(f'SELECT earning_from_referral FROM users WHERE user_id = ?', (referral_id,)).fetchone()[0]
    return referrals, earning


def get_refer_id(user_id):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    data = cur.execute('SELECT refer_id FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return data


def add_balance_by_referral(user_id, summ):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('UPDATE users SET earning_from_referral = earning_from_referral + ? WHERE user_id = ?',
                (summ, user_id,))
    con.commit()
    add_balance(user_id=user_id, plus_balance=summ)


def create_table_for_mailing(table_name):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        f'CREATE TABLE IF NOT EXISTS mailing_{table_name}(user_id INT, status VARCHAR DEFAULT "waiting", description VARCHAR)')
    cur.execute(f'INSERT INTO mailing_{table_name}(user_id) SELECT user_id FROM users WHERE role = "member"')
    con.commit()


def get_all_user_ids_for_mailing(table_name) -> list:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    user_ids = cur.execute(f'SELECT user_id FROM mailing_{table_name} WHERE status = "waiting"').fetchall()
    return list(map(lambda x: x[0], user_ids))


def change_status_for_mailing(table_name, user_id, status, description=None):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'UPDATE mailing_{table_name} SET status = ?, description = ? WHERE user_id = ?',
                (status, description, user_id,))
    con.commit()


def get_count_of_success_status(table_name) -> int:
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur.execute(f'SELECT COUNT(*) FROM mailing_{table_name} WHERE status = "success"').fetchone()[0]


def get_unique_description_error(table_name):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    unique_description = cur.execute(f'SELECT DISTINCT description FROM mailing_{table_name} WHERE description != "NULL"').fetchall()
    user_ids = cur.execute(f'SELECT user_id FROM mailing_{table_name} WHERE status = "unsuccess"').fetchall()
    return list(map(lambda x: x[0], unique_description)), list(map(lambda x: x[0], user_ids))


def delete_mailing_table(table_name):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'DROP TABLE mailing_{table_name}')
    con.commit()


def create_payment(user_id, amount, payment_method, label, status='waiting'):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('INSERT INTO payment_history(user_id, amount, payment_method, label, status) VALUES (?, ?, ?, ?, ?)', (user_id, amount, payment_method, str(label), status, ))
    scheduler_bg.add_job(func=change_status_in_payment_history, trigger='date', run_date=datetime.now() + timedelta(seconds=20), args=(str(label), 'cancel'), id=str(label))
    scheduler_bg.start()
    con.commit()


def change_status_in_payment_history(label, new_status):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('UPDATE payment_history SET status = ? WHERE label = ?', (new_status, label, ))
    con.commit()


def get_payment_status(label: str):
    path = f'..\\{__folder_for_db__}\\{name_of_db}' if __name__ == '__main__' else f'{__folder_for_db__}\\{name_of_db}'
    con = sqlite3.connect(path)
    cur = con.cursor()
    id, user_id, status = cur.execute('SELECT payment_id, user_id, status FROM payment_history WHERE label = ?', (label, )).fetchone()
    return id, user_id, status

# def generate_random_data():
#     category_id = random.randint(1, 3)
#     subcategory_id = random.randint(1, 2) if category_id == 1 else random.randint(3,
#                                                                                   4) if category_id == 2 else random.randint(
#         5, 7)
#     login = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 20)))
#     password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 20)))
#     return (category_id, subcategory_id, login, password)


if __name__ in ('database.work_with_sqlite3', '__main__'):
    create_db(name_of_db, __folder_for_db__)
