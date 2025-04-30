# main.py (обновлённый и рабочий)

import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import start, admin, booking, contact, search
from middlewares.antiflood import AntifloodMiddleware
from utils.logger import setup_logger
from dotenv import load_dotenv
from handlers import admin_update_handler

print ("🟢 KalinRentBot запущен!")
# Загружаем переменные окружения из t.env
load_dotenv("t.env")
print("OWNER_ID =", os.getenv("OWNER_ID"))

# Получаем токен из окружения
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения TOKEN не установлена")

async def main():
    setup_logger()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключение middleware
    dp.message.middleware(AntifloodMiddleware())

    # Подключение роутеров
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(booking.router)
    dp.include_router(contact.router)
    dp.include_router(search.router)
    dp.include_router(admin_update_handler.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
