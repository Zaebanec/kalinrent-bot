from aiogram import Router, types

router = Router()

@router.message(lambda message: message.text == "📞 Связаться")
async def contact_manager(message: types.Message):
    await message.answer(
        "📞 Связь с менеджером:\n\nТелефон: +7 999 999 99 99\nTelegram: @manager_contact"
    )
