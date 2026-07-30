from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database import get_balance

router = Router()


@router.message(lambda message: message.text == "👛 Wallet")
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
