from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


class DepositState(StatesGroup):
    method = State()
    usd = State()
    txid = State()


PAYMENT_METHODS = [
    "bKash",
    "Nagad",
    "Rocket",
    "Binance",
    "Bybit",
]


@router.callback_query(F.data == "deposit")
async def deposit_menu(callback: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟣 bKash", callback_data="pay_bKash")],
            [InlineKeyboardButton(text="🟠 Nagad", callback_data="pay_Nagad")],
            [InlineKeyboardButton(text="🟣 Rocket", callback_data="pay_Rocket")],
            [InlineKeyboardButton(text="🟡 Binance", callback_data="pay_Binance")],
            [InlineKeyboardButton(text="⚫ Bybit", callback_data="pay_Bybit")],
        ]
    )

    await callback.message.edit_text(
        "💳 <b>Select Deposit Method</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )

    await callback.answer()


@router.callback_query(F.data.startswith("pay_"))
async def choose_method(callback: CallbackQuery, state: FSMContext):

    method = callback.data.replace("pay_", "")

    await state.update_data(method=method)
    await state.set_state(DepositState.usd)

    await callback.message.edit_text(
        f"✅ Method: <b>{method}</b>\n\n"
        "Enter deposit amount in USD.\n\n"
        "Example:\n"
        "<code>1.5</code>",
        parse_mode="HTML",
    )

    await callback.answer()


@router.message(DepositState.usd)
async def get_usd(message: Message, state: FSMContext):

    try:
        usd = float(message.text)

        if usd < 0.20:
            await message.answer(
                "❌ Minimum deposit is $0.20"
            )
            return

    except:
        await message.answer(
            "❌ Please enter a valid USD amount."
        )
        return

    await state.update_data(usd=usd)
    await state.set_state(DepositState.txid)

    await message.answer(
        "✅ Amount received.\n\n"
        "Now send your Transaction ID (TXID)."
    )
