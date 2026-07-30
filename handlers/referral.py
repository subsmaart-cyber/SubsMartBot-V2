from aiogram import Router
from aiogram.types import Message

from database import connect

router = Router()

REFERRAL_REWARD = 0.05


@router.message(lambda message: message.text == "🎁 Referral")
async def referral(message: Message):

    bot_info = await message.bot.get_me()

    link = (
        f"https://t.me/{bot_info.username}"
        f"?start={message.from_user.id}"
    )

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT referrals
            FROM users
            WHERE user_id=?
            """,
            (message.from_user.id,)
        )

        row = await cursor.fetchone()

    total = row[0] if row else 0

    text = f"""
🎁 <b>Referral Program</b>

👥 Total Referrals: {total}

💵 Reward Per Referral:
${REFERRAL_REWARD:.2f}

🔗 Your Referral Link:

<code>{link}</code>
"""

    await message.answer(
        text,
        parse_mode="HTML"
    )
