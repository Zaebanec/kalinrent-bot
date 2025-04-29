# handlers/start.py

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.search_filters import get_filters_keyboard
from states.search_states import SearchStates

router = Router()

# Главное меню
def get_main_menu():
    keyboard = [
        [KeyboardButton(text="🔍 Поиск квартиры")],
        [KeyboardButton(text="📞 Связаться")],
        [KeyboardButton(text="ℹ️ О проекте")],
        [KeyboardButton(text="🛠 Админ-панель")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Команда /start
@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "🏡 KalinRentBot — бот для аренды лучших квартир в Калининграде!\n\nВыберите действие:",
        reply_markup=get_main_menu()
    )

# Обработка нажатия "Поиск квартиры"
@router.message(F.text == "🔍 Поиск квартиры")
async def cmd_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchStates.choosing_filters)
    await state.update_data(filters={})
    await message.answer(
        "📍 Выберите фильтры для поиска квартиры:",
        reply_markup=get_filters_keyboard()
    )
