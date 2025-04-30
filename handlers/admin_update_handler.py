from aiogram import Router, types, F
from aiogram.types import CallbackQuery
import subprocess
from keyboards.admin_inline_menu import admin_menu

router = Router()  # ← ВАЖНО: должен быть до всех @router.***

@router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    await message.answer("Добро пожаловать в админ-панель", reply_markup=admin_menu)

@router.callback_query(F.data == "admin_update_bot")
async def update_bot_callback(callback: CallbackQuery):
    await callback.answer("Обновление начато...", show_alert=False)
    try:
        result = subprocess.run(["python3", "git_push.py"], capture_output=True, text=True)

        await callback.message.answer(f"ℹ️ Результат: returncode = {result.returncode}")

        if result.returncode == 0:
            await callback.message.answer("✅ Изменения запушены. Бот скоро перезапустится.")
        elif result.returncode == 2:
            await callback.message.answer("ℹ️ Нет изменений для пуша. Всё актуально.")
        else:
            await callback.message.answer(f"⚠️ Ошибка при пуше:\\n{result.stderr}")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка запуска скрипта:\\n{e}")
