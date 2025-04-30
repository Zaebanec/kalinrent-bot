# main.py (финальная версия с гарантированным подключением admin.router)

import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import start, admin, booking, contact, search
from middlewares.antiflood import AntifloodMiddleware
from utils.logger import setup_logger

# Загрузка переменных окружения
load_dotenv("t.env")
TOKEN = os.getenv("TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

if not TOKEN:
    raise ValueError("Переменная окружения TOKEN не установлена")
if not OWNER_ID:
    print("⚠️ OWNER_ID не найден. Проверь t.env")

async def main():
    setup_logger()
    print("🟢 KalinRentBot запущен!")
    print("OWNER_ID =", OWNER_ID)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Middleware
    dp.message.middleware(AntifloodMiddleware())

    # Подключение всех роутеров
    dp.include_router(start.router)
    dp.include_router(admin.router)  # ⚠️ ОБЯЗАТЕЛЬНО до остальных, не перекрыт
    dp.include_router(booking.router)
    dp.include_router(contact.router)
    dp.include_router(search.router)

    # Стартуем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())