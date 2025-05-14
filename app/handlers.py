from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram import Router, types, F
import give_vinchik.app.keybords as kb
import os
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()

class Questionnaire(StatesGroup):
    username = State()
    description_user = State()
    photo_user = State()
    interests_user = State()

@router.message(F.text == 'Остановить создание анкеты')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply('Создание анкеты прервано. Отпраьте /reg чтобы начать сначала.')


@router.message(CommandStart())
async def cmd_hello(message: Message):
    await message.reply(
        f"Привет, <b>{message.from_user.full_name}</b>! Приступим к созданию твоей анкеты.\n Напиши в чат /reg, чтобы начать",
        parse_mode=ParseMode.HTML)

@router.message(Command('reg'))
async def user_name(message: Message, state: FSMContext):
    await state.set_state(Questionnaire.username)
    await message.answer(
        text="Введи своё имя",
        reply_markup=kb.otdaivincikBot,
        resize_keyboard=True)


@router.message(Questionnaire.username)
async def second_user_name(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.reply("Пожалуйста, введите ваше имя в виде текста.")
        return
    await state.update_data(username=message.text)
    await message.reply(
        text="Спасибо! Ваше имя было сохранено.",
        reply_markup=kb.otdaivincikBot,
        resize_keyboard=True
    )
    await state.set_state(Questionnaire.description_user)
    await message.answer(
        text="Теперь придумай описание к своей анкете.",
        reply_markup=kb.otdaivincikBot,
        resize_keyboard=True
    )


@router.message(Questionnaire.description_user)
async def user_description(message: Message, state: FSMContext):
    await state.update_data(description_user=message.text)
    await message.answer(
        text="Отлично! Отправьте ваше лучшее фото.",
        reply_markup=kb.otdaivincikBot,
        resize_keyboard=True
    )
    await state.set_state(Questionnaire.photo_user)

@router.message(Questionnaire.photo_user)
async def user_photo(message: Message, state: FSMContext):
    if message.content_type != ContentType.PHOTO:
        await message.reply('Отправьте фото!')
        return
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
    await state.update_data(photo=message.photo)
    await message.answer('Осталось лишь указать свои интересы! Напиши их через запятую.')
    await state.set_state(Questionnaire.interests_user)


@router.message(Questionnaire.interests_user)
async def user_interests(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.reply("Пожалуйста, введите ваши интересы в виде текста.")
        return
    await state.update_data(username=message.text)
    await message.reply(
        text="Ваша анкета создана. Так она выглядит:",
        reply_markup=kb.otdaivincikBot,
        resize_keyboard=True
    )
    #тут будет бот присылать сообщение полной анкеты