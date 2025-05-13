import asyncio
import os

from aiogram.enums import ParseMode, ContentType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, types, F, Bot, Dispatcher
import give_vinchik.app.keybords as kb
from dotenv import load_dotenv

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
            # Получаем фотографию с наивысшим разрешением (последний элемент в массиве)
            photo = message.photo[-1]

            # Получаем информацию о файле
            file_info = await bot.get_file(photo.file_id)

            # Скачиваем файл
            downloaded_file = await bot.download_file(file_info.file_path)

            # Задаем путь для сохранения
            save_path = "photo.jpg"

            # Сохраняем файл
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file.read())

            await message.reply("Фотография сохранена.")

        except Exception as e:
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
