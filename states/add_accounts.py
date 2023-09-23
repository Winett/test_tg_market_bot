from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAccounts(StatesGroup):
    select_category = State()
    select_subcategory = State()
    select_type_accounts = State()
    wait_data = State()