from aiogram.fsm.state import State, StatesGroup


class SearchDelForm(StatesGroup):
    tag = State()
    object = State()
    mesg = State()


class AddForm(StatesGroup):
    name = State()
    note = State()
    tag = State()
    photo = State()
