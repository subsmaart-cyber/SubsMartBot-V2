from aiogram import Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import FORCE_JOIN_CHANNEL, FORCE_JOIN_LINK

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

    kb = InlineKeyboardBuilder()
    kb.button(
        text="📢 Join Channel",
        url=FORCE_JOIN_LINK
    )

    await message.answer(
        f"""🚫 You must join our channel first.

📢 {FORCE_JOIN_CHANNEL}

After joining the channel, send /start again.""",
        reply_markup=kb.as_markup()
    )
