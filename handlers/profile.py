from aiogram import Router
from aiogram.types import Message

from database import get_balance

router = Router()


@router.message(lambda message: message.text == "👤 Profile")
async def profile(message: Message):
    user = message.from_user
    balance = await get_balance(user.id)

    text = (
        "👤 <b>Your Profile</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Name: {user.full_name}\n"
        f"📛 Username: @{user.username if user.username else 'None'}\n"
        f"💰 Wallet Balance: <b>${balance:.2f}</b>"
    )

    await message.answer(text, parse_mode="HTML")
