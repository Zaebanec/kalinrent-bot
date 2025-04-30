# handlers/admin.py (финальная сборка: добавление, удаление, обновление)

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.state import State, StatesGroup
from database.db import add_apartment, get_all_apartments, delete_apartment
import os
import subprocess

raw_id = os.getenv("OWNER_ID")
if not raw_id:
    print("⚠️ OWNER_ID не найден. Проверь t.env")
    raw_id = "0"
OWNER_ID = int(raw_id)

router = Router()

class AddApartment(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_district = State()
    waiting_for_rooms = State()
    waiting_for_photo = State()

# /admin вход в админку
@router.message(Command("admin"), F.from_user.id == OWNER_ID)
async def admin_menu(message: types.Message):
    print("✅ admin_menu сработал")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить квартиру", callback_data="add_apartment")],
        [InlineKeyboardButton(text="🗑 Удалить квартиру", callback_data="delete_apartment")],
        [InlineKeyboardButton(text="🔄 Обновить бота", callback_data="update_bot")]
    ])
    await message.answer("🔧 Добро пожаловать в админ-панель:", reply_markup=keyboard)

# Обновление бота
@router.callback_query(F.data == "update_bot")
async def update_bot(callback: types.CallbackQuery):
    result = subprocess.run(["python3", "git_push.py"], capture_output=True, text=True)
    if result.returncode == 0:
        await callback.message.answer("✅ Обновление запущено. Бот скоро перезапустится.")
    elif result.returncode == 2:
        await callback.message.answer("⚠️ Нет изменений для пуша. Бот не обновлялся.")
    else:
        await callback.message.answer("❌ Ошибка при обновлении. Посмотри логи в консоли.")
    await callback.answer()

# FSM: добавление квартиры
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

# Удаление квартиры
@router.callback_query(F.data == "delete_apartment")
async def choose_apartment_to_delete(callback: types.CallbackQuery):
    apartments = get_all_apartments()
    if not apartments:
        await callback.message.answer("⚠️ Квартир нет в базе.")
        return

    keyboard = []
    for apt in apartments:
        button = InlineKeyboardButton(
            text=f"❌ {apt['title']} (ID {apt['id']})",
            callback_data=f"confirm_delete_{apt['id']}"
        )
        keyboard.append([button])

    await callback.message.answer("Выберите квартиру для удаления:",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete(callback: types.CallbackQuery):
    apt_id = int(callback.data.replace("confirm_delete_", ""))
    delete_apartment(apt_id)
    await callback.message.answer(f"✅ Квартира с ID {apt_id} удалена.")
    await callback.answer()
