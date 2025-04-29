# keyboards/search_filters.py

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class FilterCallback(CallbackData, prefix="filter"):
    category: str
    value: str

def get_filters_keyboard():
    builder = InlineKeyboardBuilder()

    # Районы
    builder.button(text="Центральный", callback_data=FilterCallback(category="district", value="Центральный").pack())
    builder.button(text="Ленинградский", callback_data=FilterCallback(category="district", value="Ленинградский").pack())
    builder.button(text="Московский", callback_data=FilterCallback(category="district", value="Московский").pack())
    builder.button(text="Другие", callback_data=FilterCallback(category="district", value="Другие").pack())

    # Цены (новые)
    builder.button(text="до 2000", callback_data=FilterCallback(category="price", value="до 2000").pack())
    builder.button(text="2000-3500", callback_data=FilterCallback(category="price", value="2000-3500").pack())
    builder.button(text="3500-5000", callback_data=FilterCallback(category="price", value="3500-5000").pack())
    builder.button(text="5000-10000", callback_data=FilterCallback(category="price", value="5000-10000").pack())
    builder.button(text="10000+", callback_data=FilterCallback(category="price", value="10000+").pack())

    # Количество комнат
    builder.button(text="1 комн.", callback_data=FilterCallback(category="rooms", value="1").pack())
    builder.button(text="2 комн.", callback_data=FilterCallback(category="rooms", value="2").pack())
    builder.button(text="3+ комн.", callback_data=FilterCallback(category="rooms", value="3+").pack())

    # Управление
    builder.button(text="🔎 Показать квартиры", callback_data=FilterCallback(category="action", value="show").pack())
    builder.button(text="♻️ Сбросить фильтры", callback_data=FilterCallback(category="action", value="reset").pack())
    builder.button(text="📋 Показать все квартиры", callback_data=FilterCallback(category="action", value="show_all").pack())

    # Структура
    builder.adjust(2, 2, 2, 2, 2, 1, 1, 1)

    return builder.as_markup()
