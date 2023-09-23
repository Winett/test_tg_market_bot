import faker
from random import choice, randint

domains = ['mail.ru', 'yandex.ru', 'lenta.ru', 'google.com']

fake = faker.Faker(locale='ru')


def generate_random_data_for_db(times=200) -> list:
    data = []
    for i in range(times):
        category_id = randint(1, 3)
        subcategory_id = randint(1, 2) if category_id == 1 else randint(3, 4) if category_id == 2 else randint(5, 7)
        data.append((category_id, subcategory_id, fake.email(domain=choice(domains)), fake.password()))
    return data
