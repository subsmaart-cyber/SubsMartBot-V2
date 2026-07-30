from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID
from database import (
    total_users,
    total_products,
    total_deposits,
    total_purchases,
)

router = Router()


@router.message(Command("stats"))
async def stats(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    users = await total_users()
    products = await total_products()
    deposits = await total_deposits()
    purchases = await total_purchases()

    await message.answer(
        f"""
📊 <b>Shop Statistics</b>

👥 Total Users: {users}
🛒 Total Products: {products}
💳 Total Deposits: {deposits}
📦 Total Purchases: {purchases}
""",
        parse_mode="HTML"
    )
