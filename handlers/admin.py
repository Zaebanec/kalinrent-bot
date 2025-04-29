# handlers/admin.py (FSM: добавление квартиры с защитой переменной)

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters.state import State, StatesGroup
from database.db import add_apartment
import os

# OWNER_ID с безопасной проверкой окружения
raw_id = os.getenv("OWNER_ID")
if not raw_id:
    print("⚠️ OWNER_ID не найден. Проверь t.env")
    raw_id = "0"
OWNER_ID = int(raw_id)

router = Router()

# Состояния FSM для добавления квартиры
class AddApartment(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_district = State()
    waiting_for_rooms = State()
    waiting_for_photo = State()

# Кнопка запуска добавления квартиры
@router.message(Command("admin"), F.from_user.id == OWNER_ID)
async def admin_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить квартиру", callback_data="add_apartment")]
    ])
    await message.answer("🔧 Админ-панель:", reply_markup=keyboard)

@router.callback_query(F.data == "add_apartment")
async def start_add_apartment(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddApartment.waiting_for_title)
    await callback.message.answer("🏡 Введите заголовок квартиры:")
    await callback.answer()

@router.message(AddApartment.waiting_for_title)
async def add_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddApartment.waiting_for_description)
    await message.answer("📝 Введите описание квартиры:")

@router.message(AddApartment.waiting_for_description)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddApartment.waiting_for_price)
    await message.answer("💰 Введите цену за сутки (только цифры):")

@router.message(AddApartment.waiting_for_price)
async def add_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ Пожалуйста, введите только цифры!")
    await state.update_data(price=int(message.text))
    await state.set_state(AddApartment.waiting_for_district)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Центральный", callback_data="district_Центральный")],
        [InlineKeyboardButton(text="Ленинградский", callback_data="district_Ленинградский")],
        [InlineKeyboardButton(text="Московский", callback_data="district_Московский")],
        [InlineKeyboardButton(text="Другие", callback_data="district_Другие")],
    ])
    await message.answer("📍 Выберите район:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("district_"))
async def add_district(callback: types.CallbackQuery, state: FSMContext):
    district = callback.data.replace("district_", "")
    await state.update_data(district=district)
    await state.set_state(AddApartment.waiting_for_rooms)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 комн.", callback_data="rooms_1")],
        [InlineKeyboardButton(text="2 комн.", callback_data="rooms_2")],
        [InlineKeyboardButton(text="3+ комн.", callback_data="rooms_3")],
    ])
    await callback.message.answer("🚪 Выберите количество комнат:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("rooms_"))
async def add_rooms(callback: types.CallbackQuery, state: FSMContext):
    rooms = callback.data.replace("rooms_", "")
    await state.update_data(rooms=int(rooms) if rooms != "3" else 3)
    await state.set_state(AddApartment.waiting_for_photo)
    await callback.message.answer("📷 Пришлите ОДНО фото квартиры (как файл или изображение):")
    await callback.answer()

@router.message(AddApartment.waiting_for_photo, F.photo)
async def add_photo(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    data["photo"] = photo_file_id

    add_apartment(data)
    await message.answer("✅ Квартира успешно добавлена!")
    await state.clear()

@router.message(AddApartment.waiting_for_photo)
async def photo_required(message: types.Message):
    await message.answer("⚠️ Пожалуйста, отправьте именно фото квартиры.")
