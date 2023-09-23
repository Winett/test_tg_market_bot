from aiogram.dispatcher.filters.state import StatesGroup, State


class Buy(StatesGroup):
    pre_buy = State()


class Payment(StatesGroup):
    Payment_data = State()
    confirm_buying = State()


class Check_payment(StatesGroup):
    wait_confirmation = State()