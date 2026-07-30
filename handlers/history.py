from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_user_deposits

router = Router()


@router.message(Command("history"))
async def deposit_history(message: Message):

    deposits = await get_user_deposits(message.from_user.id)

    if not deposits:
        await message.answer(
            "📭 You don't have any deposit history."
        )
        return

    text = "📜 <b>Your Deposit History</b>\n\n"

    for i, deposit in enumerate(deposits, start=1):
        method, usd, status, created_at = deposit

        text += (
            f"{i}. 💳 {method}\n"
            f"💵 ${usd:.2f}\n"
            f"📌 {status}\n"
            f"🕒 {created_at}\n\n"
        )

    await message.answer(
        text,
        parse_mode="HTML"
    )
