from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "🛒 Products")
async def products(message: Message):
    text = (
        "🛒 <b>Products</b>\n\n"
        "No products available right now.\n\n"
        "Please check again later."
    )

    await message.answer(text, parse_mode="HTML")
