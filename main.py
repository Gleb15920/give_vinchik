import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv

async def main():
    load_dotenv()
    token_tg = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(token=token_tg)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')