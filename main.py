import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher
from app.handlers import setup_handlers
from dotenv import load_dotenv
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram import Router
import give_vinchik.app.keybords as kb

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


load_dotenv()
token_tg = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token_tg)
router = Router()
dp = Dispatcher()

def make_db():
    conn = sqlite3.connect('users_table.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                interests TEXT NOT NULL,
                description TEXT,
                photo TEXT NOT NULL,
                likes TEXT
            )
        ''')
    conn.commit()
    conn.close()

async def main():
    make_db()
    setup_handlers(router, bot, logging)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

