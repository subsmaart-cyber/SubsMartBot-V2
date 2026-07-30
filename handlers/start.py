from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu
from database import add_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    await add_user(
        user.id,
        user.username,
        user.full_name
    )

    await message.answer(
        "👋 Welcome to Subs Mart!\n\n"
        "Use the menu below to explore the shop.",
        reply_markup=main_menu()
    )
