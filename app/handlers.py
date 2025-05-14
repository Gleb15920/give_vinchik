import asyncio
import os

from aiogram.enums import ParseMode, ContentType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, types, F, Bot, Dispatcher
import give_vinchik.app.keybords as kb
from dotenv import load_dotenv
import logging
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()
load_dotenv()
token_tg = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token_tg)
dp = Dispatcher()

@router.message(CommandStart())
async def cmd_hello(message: Message):
    await message.reply(
        f"Привет, <b>{message.from_user.full_name}</b>! Чтобы найти новые знакомства, заполни анкету.",
        parse_mode=ParseMode.HTML)

    await message.answer(f"Нажмите:\n"
                         f"1 - Добавить фотографию\n"
                         f"2 - Добавить описание\n"
                         f"3 - Добавить искомые интересы",
                        reply_markup=kb.otdaivincikBot,
                        resize_keyboard=True,
                        input_field_placeholder='Выберите цифру')

@router.message(F.text.lower() == "1")
async def one_answ(message: types.Message):
    await message.answer("Пришлите 1 фотографию")

    @router.message(F.photo)
    async def cmd_photo(message: Message):
        try:
            # Получаем фотографию с наивысшим разрешением
            photo = message.photo[-1]
            logger.info(f"Получена фотография с file_id: {photo.file_id}")

            # Получаем информацию о файле
            file_info = await bot.get_file(photo.file_id)
            logger.info(f"Информация о файле: {file_info.file_path}")

            # Скачиваем файл
            downloaded_file = await bot.download_file(file_info.file_path)
            logger.info("Файл успешно скачан")

            # Формируем уникальное имя файла с временной меткой
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"photo_{timestamp}_{photo.file_id}.jpg"

            # Проверяем права на запись в директорию
            save_dir = os.path.dirname(save_path) or "."
            if not os.access(save_dir, os.W_OK):
                logger.error(f"Нет прав на запись в директорию: {save_dir}")
                await message.reply("Ошибка: Нет прав на запись в директорию.")
                return

            # Сохраняем файл
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file.read())

            # Проверяем, существует ли файл
            if os.path.exists(save_path):
                logger.info(f"Фотография сохранена как {save_path}")
                await message.reply(f"Фотография сохранена как {save_path}.")
            else:
                logger.error("Файл не был сохранен")
                await message.reply("Ошибка: Файл не был сохранен.")

        except Exception as e:
            logger.error(f"Ошибка при обработке фотографии: {str(e)}")
            await message.reply(f"Ошибка при сохранении фотографии: {str(e)}")

    @router.message(F.content_type != ContentType.PHOTO)
    async def handle_non_photo(message: types.Message):
        await message.reply("Это не фото")

@router.message(F.text.lower() == "2")
async def two_answ(message: types.Message):
    await message.answer("Пришлите описание анкеты")

@router.message(F.text.lower() == "3")
async def three_answ(message: types.Message):
    await message.answer("Напишите искомые интересы")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
