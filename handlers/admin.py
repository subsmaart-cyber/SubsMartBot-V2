from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import (
    add_product,
    add_stock,
    total_users,
    total_products,
    total_deposits,
    total_purchases,
)

router = Router()


def is_admin(user_id: int):
    return user_id == ADMIN_ID


class AddProductState(StatesGroup):
    name = State()
    price = State()
    description = State()


class AddStockState(StatesGroup):
    product_id = State()
    accounts = State()


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

👥 Users : {users}
🛒 Products : {products}
💳 Deposits : {deposits}
📦 Purchases : {purchases}

━━━━━━━━━━━━━━

/addproduct
/addstock
/stats
/broadcast
/maintenance
"""

    await message.answer(
        text,
        parse_mode="HTML"
    )


@router.message(Command("addproduct"))
async def add_product_start(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    await state.set_state(AddProductState.name)
    await message.answer("Send Product Name")


@router.message(AddProductState.name)
async def product_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await state.set_state(AddProductState.price)

    await message.answer("Send Product Price (USD)")


@router.message(AddProductState.price)
async def product_price(message: Message, state: FSMContext):

    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Invalid Price")
        return

    await state.update_data(price=price)

    await state.set_state(AddProductState.description)

    await message.answer("Send Product Description")

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
        f"✅ Product Added\n\nProduct ID: {product_id}"
    )


@router.message(Command("addstock"))
async def add_stock_start(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    await state.set_state(AddStockState.product_id)
    await message.answer("📦 Send Product ID")


@router.message(AddStockState.product_id)
async def stock_product_id(message: Message, state: FSMContext):

    try:
        product_id = int(message.text)
    except ValueError:
        await message.answer("❌ Invalid Product ID")
        return

    await state.update_data(product_id=product_id)

    await state.set_state(AddStockState.accounts)

    await message.answer(
        "📋 Send Accounts\n\n"
        "One account per line.\n\n"
        "Example:\n"
        "email1@gmail.com:password1\n"
        "email2@gmail.com:password2"
    )


@router.message(AddStockState.accounts)
async def stock_accounts(message: Message, state: FSMContext):

    data = await state.get_data()
    product_id = data["product_id"]

    accounts = [
        x.strip()
        for x in message.text.splitlines()
        if x.strip()
    ]

    added = 0

    for account in accounts:
        await add_stock(product_id, account)
        added += 1

    await state.clear()

    await message.answer(
        f"""✅ Stock Added Successfully

📦 Product ID: {product_id}

➕ Added: {added}
"""
    )
