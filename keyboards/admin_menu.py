from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_main_menu():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="➕ Добавить квартиру")],
        [KeyboardButton(text="🗑 Удалить квартиру")],
        [KeyboardButton(text="🏠 Главное меню")]
    ], resize_keyboard=True)
    return keyboard
