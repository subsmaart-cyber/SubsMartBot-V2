from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_user_deposits

router = Router()


@router.callback_query(lambda c: c.data == "deposit_history")
async def deposit_history(callback: CallbackQuery):

    deposits = await get_user_deposits(callback.from_user.id)

    if not deposits:
        await callback.message.answer(
            "📭 You don't have any deposit history."
        )
        await callback.answer()
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

    await callback.message.answer(
        text,
        parse_mode="HTML"
    )

    await callback.answer()
