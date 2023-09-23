from aiogram.dispatcher.filters.state import StatesGroup, State


class EditCategory(StatesGroup):
    wait_category_for_editing = State()
    wait_new_category_name = State()


class AddCategory(StatesGroup):
    wait_new_category = State()
