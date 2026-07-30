import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from database import init_db

load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
