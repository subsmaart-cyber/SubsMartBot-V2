from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database import (
    get_balance,
    get_user_deposits,
)

router = Router()


@router.message(F.text == "👛 Wallet")
async def wallet(message: Message):

    balance = await get_balance(message.from_user.id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Deposit",
                    callback_data="deposit"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 Deposit History",
                    callback_data="deposit_history"
                )
            ]
        ]
    )

    await message.answer(
        f"👛 <b>Your Wallet</b>\n\n"
        f"💰 Balance: <b>${balance:.2f}</b>",
        parse_mode="HTML",
        reply_markup=keyboard
    )


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
