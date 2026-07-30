import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import init_db
from handlers import register_handlers

load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def main():
    await init_db()
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
