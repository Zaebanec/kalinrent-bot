# handlers/search.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.search_filters import get_filters_keyboard, FilterCallback
from states.search_states import SearchStates
from database.db import find_apartments
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text == "🔍 Поиск квартиры")
async def start_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchStates.choosing_filters)
    await state.update_data(filters={})
    await message.answer(
        "📍 Выберите фильтры для поиска квартиры:",
        reply_markup=get_filters_keyboard()
    )

@router.callback_query(FilterCallback.filter())
async def process_filter(callback: types.CallbackQuery, callback_data: FilterCallback, state: FSMContext):
    data = await state.get_data()
    filters = data.get("filters", {})

    if callback_data.category in ["district", "price", "rooms"]:
        filters[callback_data.category] = callback_data.value
        await state.update_data(filters=filters)
        await callback.answer(f"Вы выбрали: {callback_data.value}")

    elif callback_data.category == "action":
        if callback_data.value == "show":
            await show_apartments(callback, filters)
            await state.clear()
        elif callback_data.value == "reset":
            await state.update_data(filters={})
            await callback.message.edit_text(
                "📍 Выберите фильтры для поиска квартиры:",
                reply_markup=get_filters_keyboard()
            )
            await callback.answer()

async def show_apartments(callback: types.CallbackQuery, filters: dict):
    apartments = find_apartments(filters)

    if not apartments:
        await callback.message.edit_text(
            "❌ Квартиры по вашему запросу не найдены.\n\nПопробуйте изменить фильтры:",
            reply_markup=get_filters_keyboard()
        )
        return

    for apt in apartments:
        text = (
            f"🏠 <b>{apt['title']}</b>\n"
            f"📍 Район: {apt['district']}\n"
            f"💵 Цена: {apt['price']} ₽\n"
            f"🛏 Комнат: {apt['rooms']}\n"
            f"📝 Описание: {apt['description']}"
        )

        apartment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗓️ Забронировать",
                    callback_data=f"book_{apt['id']}"
                ),
                InlineKeyboardButton(
                    text="📞 Связаться",
                    callback_data=f"contact_{apt['id']}"
                )
            ]
        ])

        if apt.get('photo'):
            try:
                await callback.message.answer_photo(
                    photo=apt['photo'],
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=apartment_keyboard
                )
            except Exception as e:
                print(f"Ошибка при отправке фото: {e}")
                await callback.message.answer(
                    text,
                    parse_mode="HTML",
                    reply_markup=apartment_keyboard
                )
        else:
            await callback.message.answer(
                text,
                parse_mode="HTML",
                reply_markup=apartment_keyboard
            )

    await callback.answer()

@router.callback_query(F.data.startswith("book_"))
async def book_apartment(callback: types.CallbackQuery):
    apartment_id = callback.data.replace("book_", "")
    await callback.answer()
    await callback.message.answer(f"🗓️ Вы хотите забронировать квартиру №{apartment_id}. Менеджер свяжется с вами!")

@router.callback_query(F.data.startswith("contact_"))
async def contact_apartment(callback: types.CallbackQuery):
    apartment_id = callback.data.replace("contact_", "")
    await callback.answer()
    await callback.message.answer(f"📞 Связаться по квартире №{apartment_id}:\n\nТелефон: +7 999 999 99 99\nTelegram: @manager_contact")
