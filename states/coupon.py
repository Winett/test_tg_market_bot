from aiogram.dispatcher.filters.state import StatesGroup, State

class CreateCoupon(StatesGroup):
    name_coupon = State()
    amount = State()
    expiration_date = State()