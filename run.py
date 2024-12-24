import asyncio
from main import *


async def main() -> None:
    print("Starting...")
    await dp.start_polling(bot)


asyncio.run(main())
