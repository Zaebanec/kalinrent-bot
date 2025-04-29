# states/search_states.py

from aiogram.fsm.state import StatesGroup, State

class SearchStates(StatesGroup):
    choosing_filters = State()
