from aiogram import Router, F
from aiogram.types import Message

from database import get_reviews

router = Router()


@router.message(F.text == "⭐ Reviews")
async def reviews(message: Message):

    reviews = await get_reviews()

    if not reviews:
        await message.answer("⭐ No reviews yet.")
        return

    text = "⭐ <b>Customer Reviews</b>\n\n"

    for name, review in reviews:
        text += f"👤 <b>{name}</b>\n💬 {review}\n\n"

    await message.answer(
        text,
        parse_mode="HTML"
    )
