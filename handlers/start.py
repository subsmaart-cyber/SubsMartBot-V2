from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu

from database import (
    add_user,
    has_referrer,
    set_referrer,
    reward_referrer
)

from config import REFERRAL_REWARD

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    user = message.from_user

    await add_user(
        user.id,
        user.username,
        user.full_name
    )

    args = message.text.split()

    if len(args) > 1:

        try:
            referrer_id = int(args[1])

            if (
                referrer_id != user.id
                and not await has_referrer(user.id)
            ):

                await set_referrer(
                    user.id,
                    referrer_id
                )

                await reward_referrer(
                    referrer_id,
                    REFERRAL_REWARD
                )

        except Exception:
            pass

    await message.answer(
        "👋 Welcome to Subs Mart!\n\n"
        "Use the menu below to explore the shop.",
        reply_markup=main_menu()
    )
