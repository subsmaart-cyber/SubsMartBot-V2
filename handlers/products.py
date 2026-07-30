from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("products"))
async def products(message: Message):
    await message.answer("🛒 Products")
