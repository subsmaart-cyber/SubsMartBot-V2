from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "👤 Profile")
async def profile(message: Message):
    user = message.from_user

    text = (
        "👤 <b>Your Profile</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Name: {user.full_name}\n"
        f"📛 Username: @{user.username if user.username else 'None'}"
    )

    await message.answer(text, parse_mode="HTML")
