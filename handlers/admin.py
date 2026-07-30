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


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):

    if not is_admin(message.from_user.id):
        return

    users = await total_users()
    products = await total_products()
    deposits = await total_deposits()
    purchases = await total_purchases()

    text = f"""
🛠 <b>Subs Mart Admin Panel</b>

👥 Users: {users}
🛒 Products: {products}
💳 Deposits: {deposits}
📦 Purchases: {purchases}

━━━━━━━━━━━━━━

Available Commands

/addproduct
/addstock
/broadcast
/stats
/maintenance
"""

    await message.answer(
        text,
        parse_mode="HTML"
    )
