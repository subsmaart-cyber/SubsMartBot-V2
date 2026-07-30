from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("wallet"))
async def wallet(message: Message):
    await message.answer("👛 Wallet")
