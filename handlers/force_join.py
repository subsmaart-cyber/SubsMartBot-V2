from aiogram import Router
from aiogram.types import Message

from config import FORCE_JOIN_CHANNEL

router = Router()


async def check_force_join(bot, user_id):

    try:
        member = await bot.get_chat_member(
            FORCE_JOIN_CHANNEL,
            user_id
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except Exception:
        return False


@router.message()
async def force_join(message: Message):

    joined = await check_force_join(
        message.bot,
        message.from_user.id
    )

    if joined:
        return

    await message.answer(
        f"""
🚫 You must join our channel first.

📢 {FORCE_JOIN_CHANNEL}

After joining, send any message again.
"""
    )
