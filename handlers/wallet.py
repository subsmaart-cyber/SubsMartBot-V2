from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "👛 Wallet")
async def wallet(message: Message):
    text = (
        "👛 <b>Wallet</b>\n\n"
        "💰 Balance: <b>$0.00</b>\n\n"
        "Select an option:\n"
        "• Deposit\n"
        "• Deposit History"
    )

    await message.answer(text, parse_mode="HTML")
