from aiogram.fsm.state import StatesGroup, State


class User:
    user_id = State()
    name = State()
    interest = State()
    likes = State()
