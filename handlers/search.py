# handlers/search.py (с отладкой и защитой отображения квартир)

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from filters.callback_data import FilterCallback
from states.search_states import SearchStates
from database.db import find_apartments
from keyboards.search_filters import get_filters_keyboard

router = Router()

# Команда выбора фильтров
@router.message(F.text == "🔍 Поиск квартиры")
async def cmd_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchStates.choosing_filters)
    await state.update_data(filters={})
    await message.answer("📍 Выберите фильтры для поиска квартиры:", reply_markup=get_filters_keyboard())

# Обработка выбора фильтров через inline-кнопки
@router.callback_query(FilterCallback.filter())
async def process_filter(callback: types.CallbackQuery, callback_data: FilterCallback, state: FSMContext):
    data = await state.get_data()
    filters = data.get("filters", {})

    if callback_data.category == "district":
        filters["district"] = callback_data.value
        await callback.answer(f"Вы выбрали район: {callback_data.value}")

    elif callback_data.category == "price":
        filters["price"] = callback_data.value
        await callback.answer(f"Вы выбрали цену: {callback_data.value}")

    elif callback_data.category == "rooms":
        filters["rooms"] = callback_data.value
        await callback.answer(f"Вы выбрали комнат: {callback_data.value}")

    elif callback_data.category == "action" and callback_data.value == "show":
        print("✅ Обработка показа квартир с фильтрами:", filters)
        await show_apartments(callback, filters)
        await state.clear()
        return

    await state.update_data(filters=filters)

# Показ квартир (включая лог и защиту)
async def show_apartments(callback: types.CallbackQuery, filters: dict):
    try:
        apartments = find_apartments(filters)
        print(f"🔍 show_apartments: найдено {len(apartments)} квартир")

        if not apartments:
            await callback.message.answer("❌ Квартиры по вашему запросу не найдены.")
            return

        for apt in apartments:
            text = (
                f"🏡 <b>{apt['title']}</b>\n"
                f"{apt['description']}\n\n"
                f"💵 <b>{apt['price']}</b> руб/сутки\n"
                f"📍 Район: {apt['district']}\n"
                f"🚪 Комнат: {apt['rooms']}"
            )
            try:
                await callback.message.answer_photo(photo=apt['photo'], caption=text, parse_mode="HTML")
            except Exception as e:
                print("⚠️ Ошибка при отправке квартиры:", e)
                await callback.message.answer(text, parse_mode="HTML")

    except Exception as e:
        print("❌ Ошибка в show_apartments:", e)
        await callback.message.answer("Произошла ошибка при загрузке квартир. Попробуйте ещё раз.")
