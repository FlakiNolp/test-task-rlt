import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.application.middlewaries.mongodb_middleware import MongoMiddleware
from src.application.sample.handlers import router
from src.settings.config import config

dp = Dispatcher()
dp.update.middleware(MongoMiddleware())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(config.TOKEN)

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
