import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram import Router, types, F
import give_vinchik.app.keybords as kb


async def main():
    make_db()
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
