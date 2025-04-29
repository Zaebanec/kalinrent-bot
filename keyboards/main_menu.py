from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔍 Поиск квартиры")],
        [KeyboardButton(text="📞 Связаться"), KeyboardButton(text="ℹ️ О проекте")],
        [KeyboardButton(text="🛠 Админ-панель")]
    ], resize_keyboard=True)
    return keyboard
