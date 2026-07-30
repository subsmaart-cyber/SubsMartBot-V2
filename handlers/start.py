from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Welcome to Subs Mart!\n\n"
        "Use the menu below to explore the shop."
    )
