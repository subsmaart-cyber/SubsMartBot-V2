from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID
from database import connect

router = Router()


@router.message(Command("broadcast"))
async def broadcast(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast", "", 1).strip()

    if not text:
        await message.answer(
            "Usage:\n/broadcast Your message"
        )
        return

    sent = 0
    failed = 0

    async with await connect() as db:

        cursor = await db.execute(
            "SELECT user_id FROM users"
        )

        users = await cursor.fetchall()

    for user in users:

        try:
            await message.bot.send_message(
                user[0],
                text
            )
            sent += 1

        except:
            failed += 1

    await message.answer(
        f"""
✅ Broadcast Finished

Sent: {sent}

Failed: {failed}
"""
    )
