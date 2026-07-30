from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database import (
    get_products,
    get_product,
    get_stock_count,
)

router = Router()


@router.message(lambda message: message.text == "🛒 Products")
async def products(message: Message):

    products = await get_products()

    if not products:
        await message.answer("❌ No products available.")
        return

    keyboard = []

    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product[1]} - ${product[2]:.2f}",
                callback_data=f"product_{product[0]}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="🏠 Back",
            callback_data="home"
        )
    ])

    await message.answer(
        "🛒 <b>Select a Product</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )


@router.callback_query(F.data.startswith("product_"))
async def product_details(callback: CallbackQuery):

    product_id = int(callback.data.split("_")[1])

    product = await get_product(product_id)

    if not product:
        await callback.answer("Product not found.")
        return

    stock = await get_stock_count(product_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Buy Now",
                    callback_data=f"buy_{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data="products"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        f"""
🛒 <b>{product[1]}</b>

💵 Price: ${product[2]:.2f}

📦 Stock: {stock}

📝 Description:

{product[3] if product[3] else 'No description available.'}
""",
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()
