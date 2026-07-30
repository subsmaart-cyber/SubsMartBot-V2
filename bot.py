from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

from config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


async def main():
    print("✅ SubsMart Bot V2 Started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
