from aiogram.dispatcher.filters.state import StatesGroup, State

class AdditionBalance(StatesGroup):
    wait_method_payment = State()
    wait_value_for_adding = State()
    wait_confirm = State()