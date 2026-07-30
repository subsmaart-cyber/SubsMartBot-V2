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
  from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database import add_product


class AddProductState(StatesGroup):
    name = State()
    price = State()
    description = State()


@router.message(Command("addproduct"))
async def add_product_cmd(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AddProductState.name)
    await message.answer("📝 Send product name.")


@router.message(AddProductState.name)
async def product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProductState.price)
    await message.answer("💰 Send product price (USD).")


@router.message(AddProductState.price)
async def product_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("❌ Invalid price.")
        return

    await state.update_data(price=price)
    await state.set_state(AddProductState.description)
    await message.answer("📝 Send product description.")


@router.message(AddProductState.description)
async def product_description(message: Message, state: FSMContext):
    data = await state.get_data()

    product_id = await add_product(
        data["name"],
        data["price"],
        message.text
    )

    await state.clear()

    await message.answer(
        f"✅ Product Added Successfully!\n\n"
        f"🆔 Product ID: {product_id}"
    )  
