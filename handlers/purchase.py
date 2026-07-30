from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import (
    get_balance,
    get_product,
    get_available_stock,
    mark_stock_sold,
    add_purchase,
    update_balance,
)

router = Router()


@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery):

    product_id = int(callback.data.split("_")[1])

    product = await get_product(product_id)

    if not product:
        await callback.answer("Product not found.", show_alert=True)
        return

    balance = await get_balance(callback.from_user.id)

    price = float(product[2])

    if balance < price:
        await callback.answer(
            "❌ Insufficient wallet balance.",
            show_alert=True
        )
        return

    stock = await get_available_stock(product_id)

    if not stock:
        await callback.answer(
            "❌ Product is out of stock.",
            show_alert=True
        )
        return

    await update_balance(callback.from_user.id, -price)

    await mark_stock_sold(stock[0])

    await add_purchase(
        callback.from_user.id,
        product_id,
        stock[1],
        price
    )

    await callback.message.answer(
        f"""
✅ Purchase Successful

📦 Product:
{product[1]}

💰 Paid:
${price:.2f}

━━━━━━━━━━━━━━

🔑 Your Account:

<code>{stock[1]}</code>

━━━━━━━━━━━━━━

⚠️ Save this account now
