import asyncio
from main import *
from presentation import *


async def main() -> None:
    from aiogram import Bot
    bot = Bot(token=TOKEN)
    print("Starting...")
    await dp.start_polling(bot)


asyncio.run(main())
