# keyboards/calendar_keyboard.py (фикс визуала нижнего ряда)

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import calendar

# Генерация клавиатуры календаря на текущий месяц
def generate_calendar_keyboard():
    builder = InlineKeyboardBuilder()

    now = datetime.now()
    year = now.year
    month = now.month

    # Заголовок месяца (отдельной строкой)
    builder.row(
        InlineKeyboardButton(
            text=f"📅 {calendar.month_name[month]} {year}",
            callback_data="ignore"
        )
    )

    # Дни недели
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    builder.row(*[InlineKeyboardButton(text=day, callback_data="ignore") for day in week_days])

    # Пустые ячейки до первого дня месяца
    week_day_first = calendar.monthrange(year, month)[0]
    days = []
    for _ in range(week_day_first):
        days.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    # Сами дни месяца
    month_days = calendar.monthrange(year, month)[1]
    for day in range(1, month_days + 1):
        days.append(
            InlineKeyboardButton(
                text=str(day),
                callback_data=f"select_day_{day}"
            )
        )

    # Разбивка по строкам без добивки пустыми
    row = []
    for idx, btn in enumerate(days, 1):
        row.append(btn)
        if idx % 7 == 0:
            builder.row(*row)
            row = []
    if row:
        builder.row(*row)

    return builder.as_markup()

IGNORE_CALLBACK = "ignore"
