from aiogram.dispatcher.filters.state import StatesGroup, State

class ActivateCoupon(StatesGroup):
    wait_coupon = State()