# handlers/booking.py (обновлённый фикс для даты)

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.state import State, StatesGroup
from keyboards.calendar_keyboard import generate_calendar_keyboard, IGNORE_CALLBACK
from datetime import datetime  # ✅ фикс

router = Router()

class BookingStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_date_select = State()
    waiting_for_nights = State()
    waiting_for_comment = State()
    confirmation = State()

@router.callback_query(F.data.startswith("book_"))
async def start_booking(callback: types.CallbackQuery, state: FSMContext):
    apartment_id = callback.data.replace("book_", "")
    await state.update_data(apartment_id=apartment_id)
    await state.set_state(BookingStates.waiting_for_name)
    await callback.message.answer("👤 Пожалуйста, введите ваше имя:")
    await callback.answer()

@router.message(BookingStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.waiting_for_phone)
    await message.answer("📞 Введите ваш номер телефона:")

@router.message(BookingStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(BookingStates.waiting_for_date_select)
    await message.answer("📅 Выберите дату заезда:", reply_markup=generate_calendar_keyboard())

@router.callback_query(F.data.startswith("select_day_"))
async def process_date_selection(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data.replace("select_day_", "")
    now = datetime.now()
    date_string = f"{day.zfill(2)}.{now.month:02}.{now.year}"
    await state.update_data(dates=date_string)
    await state.set_state(BookingStates.waiting_for_nights)
    await callback.message.answer("🌙 На сколько ночей планируете остаться?")
    await callback.answer()

@router.callback_query(F.data == IGNORE_CALLBACK)
async def ignore_callback(callback: types.CallbackQuery):
    await callback.answer()

@router.message(BookingStates.waiting_for_nights)
async def process_nights(message: types.Message, state: FSMContext):
    await state.update_data(nights=message.text)
    await state.set_state(BookingStates.waiting_for_comment)
    await message.answer("💬 Добавьте комментарий (если есть) или напишите '-'")

@router.message(BookingStates.waiting_for_comment)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()

    text = (
        f"🏡 <b>Бронирование квартиры №{data['apartment_id']}</b>\n\n"
        f"👤 <b>Имя:</b> {data['name']}\n"
        f"📞 <b>Телефон:</b> {data['phone']}\n"
        f"📅 <b>Дата заезда:</b> {data['dates']}\n"
        f"🌙 <b>Количество ночей:</b> {data['nights']}\n"
        f"💬 <b>Комментарий:</b> {data['comment']}"
    )

    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_booking"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_booking")
        ]
    ])

    await message.answer(text, parse_mode="HTML", reply_markup=confirm_keyboard)
    await state.set_state(BookingStates.confirmation)

@router.callback_query(F.data == "confirm_booking")
async def confirm_booking(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    text = (
        f"🔔 <b>Новая заявка на бронирование!</b>\n\n"
        f"🏡 Квартира №{data['apartment_id']}\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📅 Дата заезда: {data['dates']}\n"
        f"🌙 Ночей: {data['nights']}\n"
        f"💬 Комментарий: {data['comment']}"
    )

    await callback.message.answer(text, parse_mode="HTML")
    await state.clear()
    await callback.answer("✅ Бронирование подтверждено!")

@router.callback_query(F.data == "cancel_booking")
async def cancel_booking(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Бронирование отменено.")
    await callback.answer()
