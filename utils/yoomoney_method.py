import requests
from pprint import pprint
from data.config import client_id, yoomoney_token, transfer_yoomoney_fee
from datetime import datetime
from yoomoney import Quickpay
from uuid import uuid4


def create_transaction(summ: float | int, label=uuid4(), receiver=4100117890101609):
    quickpay = Quickpay(
        receiver=receiver,
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=float(summ) * (1.0 + transfer_yoomoney_fee / 100),
        label=label,
    )
    return label, quickpay.redirected_url


headers = {'Authorization': f'Bearer {yoomoney_token}', 'Content-Type': 'application/x-www-form-urlencoded'}

session = requests.Session()
session.headers = headers


def account_info():
    response = session.post('https://yoomoney.ru/api/account-info')
    return response.json()


def operation_history(type='deposition', label=None, from_: datetime = None):
    '''

    :param label: Для поиска оплаты
    :param type: deposition("Входные платежи на аккаунт, +(плюс) деньги") или payment("Исходящие платежи -(минус) деньги")
    :return:
    '''
    response = session.post('https://yoomoney.ru/api/operation-history',
                            data={'label': label, "type": type})
    return response.json()


def operation_details(operation_id) -> dict:
    response = session.post('https://yoomoney.ru/api/operation-details', data={'operation_id': operation_id})
    return response.json()

