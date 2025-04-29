from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def apartment_actions_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Забронировать", callback_data="book")],
        [InlineKeyboardButton(text="➡️ Следующая", callback_data="next_apartment")],
        [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
    ])
    return keyboard

def booking_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_booking")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_booking")]
    ])
    return keyboard
