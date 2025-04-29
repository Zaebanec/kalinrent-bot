# KalinRentBot — Telegram-бот для аренды квартир

## Быстрый старт:

1. Установить зависимости:
   pip install aiogram python-dotenv

2. Структура проекта:
   - main.py
   - handlers/
   - keyboards/
   - database/
   - utils/
   - middlewares/
   - t.env
   - kalinrent.db (создать базу SQLite)

3. Создать базу данных:
   Структура таблицы apartments:
   
   CREATE TABLE apartments (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     title TEXT NOT NULL,
     description TEXT NOT NULL,
     price INTEGER NOT NULL,
     district TEXT NOT NULL,
     rooms INTEGER NOT NULL,
     photo TEXT
   );

4. Запуск бота:
   python main.py

5. Всё готово к работе! 🚀
# test webhook
