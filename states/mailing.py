from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    wait_name_of_mailing = State()
    wait_message_to_mailing = State()
    use_button_for_mailing = State()
    wait_message_for_button = State()
    wait_url_for_button = State()
    pre_message_to_mailing = State()


