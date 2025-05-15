import random

from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram import Router, types, F
import give_vinchik.app.keybords as kb
import os
from datetime import datetime
import give_vinchik.user as user

router1 = None
bot1 = None
logging1 = None


def user_register(tg_id, username, interests, description, photo):
    return user.User(tg_id, username, interests, description, photo)


def setup_handlers(router, bot, logger):
    class Questionnaire(StatesGroup):
        username = State()
        description_user = State()
        photo_user = State()
        interests_user = State()

    class Changes(StatesGroup):
        username = State()
        description_user = State()
        photo_user = State()
        interests_user = State()
        lenta = State()

    @router.message(F.text == 'Остановить создание анкеты')
    async def cancel_handler(message: types.Message, state: FSMContext):
        await state.clear()
        await message.reply('Создание анкеты прервано. Отпраьте /reg чтобы начать сначала.')

    @router.message(CommandStart())
    async def cmd_hello(message: Message):
        us = user.get_user(message.from_user.id)
        if not us:
            await message.reply(
                f"Привет, <b>{message.from_user.full_name}</b>! Приступим к созданию твоей анкеты."
                f"\nНапиши в чат /reg, чтобы начать.",
                parse_mode=ParseMode.HTML)
            del us
        else:
            await message.reply(
                f"Привет, <b>{str(us.name)}</b>! Самое время поискать новых друзей по интересам!"
                f"\nНапиши в чат /lenta, чтобы начать."
                f"\nНапиши в чат /reg, чтобы создать анкету заново.",
                parse_mode=ParseMode.HTML,
                reply_markup=kb.registred_user,
                resize_keyboard=True
            )
            del us

    @router.message(Command('reg'))
    async def user_name(message: Message, state: FSMContext):
        await state.set_state(Questionnaire.username)
        await message.answer(
            text="Введи своё имя.",
            reply_markup=kb.otdaivincikBot,
            resize_keyboard=True)

    @router.message(Command('delete'))
    async def user_name(message: Message, state: FSMContext):
        user.get_user(message.from_user.id).delete_user()
        await message.answer(
            text="Пользователь удален. Возвращайтесь скорее!(",
            reply_markup=None,
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
            photo = message.photo[-1]
            logger.info(f"Получена фотография с file_id: {photo.file_id}")

            file_info = await bot.get_file(photo.file_id)
            logger.info(f"Информация о файле: {file_info.file_path}")

            downloaded_file = await bot.download_file(file_info.file_path)
            logger.info("Файл успешно скачан")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"data/photo_{timestamp}_{photo.file_id}.jpg"

            save_dir = os.path.dirname(save_path) or "."
            if not os.access(save_dir, os.W_OK):
                logger.error(f"Нет прав на запись в директорию: {save_dir}")
                await message.reply("Ошибка: Нет прав на запись в директорию.")
                return

            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file.read())

            if os.path.exists(save_path):
                logger.info(f"Фотография сохранена как {save_path}")
                await state.update_data(photo=save_path)
                await message.reply(f"Фотография успешно сохранена!")
            else:
                logger.error("Файл не был сохранен")
                await message.reply("Файл не был сохранен.")

        except Exception as e:
            logger.error(f"Ошибка при обработке фотографии: {str(e)}")
        await message.answer('Осталось лишь указать свои интересы! Напиши их через запятую. Таким образом: "хоккей, '
                             'готовка, рыбалка,..."')
        await state.set_state(Questionnaire.interests_user)

    @router.message(Questionnaire.interests_user)
    async def user_interests(message: Message, state: FSMContext):
        if message.content_type != ContentType.TEXT:
            await message.reply("Пожалуйста, введите ваши интересы в виде текста.")
            return
        await state.update_data(interests=message.text.split(", "))
        data = await state.get_data()
        tg_id = message.from_user.id
        username = data.get("username")
        interests = data.get("interests")
        description = data.get("description_user")
        photo = data.get("photo")
        us = user_register(tg_id, username, interests, description, photo)
        await state.clear()
        await message.reply(text="Ваша анкета создана. Так она выглядит:",
                            reply_markup=kb.registred_user,
                            resize_keyboard=True
                            )
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=FSInputFile(us.photo),
            caption=f"{us.name}, {us.description}",
        )
        # await message.reply(
        #     text=f"Ваша анкета создана. Так она выглядит:\n\n"
        #          f"{}",
        #     reply_markup=kb.registred_user,
        #     resize_keyboard=True
        # )

    @router.message(F.text.contains('Изменить имя'))
    async def change_name(message: Message, state: FSMContext):
        await state.set_state(Changes.username)
        await message.answer(
            text="Введи новое имя.",
            reply_markup=kb.change,
            resize_keyboard=True)

    @router.message(Changes.username)
    async def process_name(message: Message, state: FSMContext):
        if message.text == "Отмена":
            await state.clear()
            await message.answer(
                text="Отменено.",
                reply_markup=kb.registred_user,
                resize_keyboard=True)
            return
        if message.content_type != ContentType.TEXT:
            await message.reply(
                text="Описание должно быть текстом. Попробуйте снова.",
                reply_to_message_id=message.message_id
            )
            return
        name = message.text.strip()
        user.get_user(message.from_user.id).change_name(name)
        await message.reply(
            text="Спасибо! Новое имя было сохранено!",
            reply_to_message_id=message.message_id,
            reply_markup=kb.registred_user
        )
        await state.clear()

    @router.message(F.text.contains('Изменить описание'))
    async def change_description(message: Message, state: FSMContext):
        await state.set_state(Changes.description_user)
        await message.answer(
            text="Введи новое описание.",
            reply_markup=kb.change,
            resize_keyboard=True)

    @router.message(Changes.description_user)
    async def process_description(message: Message, state: FSMContext):
        if message.text == "Отмена":
            await message.answer(
                text="Отменено.",
                reply_markup=kb.registred_user,
                resize_keyboard=True)
            await state.clear()
            return
        if message.content_type != ContentType.TEXT:
            await message.reply(
                text="Описание должно быть текстом. Попробуйте снова.",
                reply_to_message_id=message.message_id
            )
            return
        description = message.text.strip()
        user.get_user(message.from_user.id).change_description(description)
        await message.reply(
            text="Спасибо! Новое описание было сохранено!",
            reply_to_message_id=message.message_id,
            reply_markup=kb.registred_user
        )
        await state.clear()

    @router.message(F.text.contains('Изменить список интересов'))
    async def change_interests(message: Message, state: FSMContext):
        await state.set_state(Changes.interests_user)
        await message.answer(
            text='Введи новый список интересов через запятую. Таким образом: "хоккей, айти, спать,..."',
            reply_markup=kb.change,
            resize_keyboard=True)

    @router.message(Changes.interests_user)
    async def process_interests(message: Message, state: FSMContext):
        if message.text == "Отмена":
            await state.clear()
            await message.answer(
                text="Отменено.",
                reply_markup=kb.registred_user,
                resize_keyboard=True)
        if message.content_type != ContentType.TEXT:
            await message.reply(
                text="Список интересов должен быть текстом. Попробуйте снова.",
                reply_to_message_id=message.message_id
            )
            return
        interests = message.text.strip().split(", ")
        user.get_user(message.from_user.id).change_interests(interests)
        await message.reply(
            text="Спасибо! Новый список интересов был сохранен!",
            reply_to_message_id=message.message_id,
            reply_markup=kb.registred_user
        )
        await state.clear()

    @router.message(F.text.contains('Поменять фотографию'))
    async def change_photo(message: Message, state: FSMContext):
        await state.set_state(Changes.photo_user)
        await message.answer(
            text="Отправьте новое фото.",
            reply_markup=kb.change,
            resize_keyboard=True)

    @router.message(Changes.photo_user)
    async def process_photo(message: Message, state: FSMContext):
        if message.text == "Отмена":
            await state.clear()
            await message.answer(
                text="Отменено.",
                reply_markup=kb.registred_user,
                resize_keyboard=True)
            return
        try:
            photo = message.photo[-1]
            logger.info(f"Получена фотография с file_id: {photo.file_id}")

            file_info = await bot.get_file(photo.file_id)
            logger.info(f"Информация о файле: {file_info.file_path}")

            downloaded_file = await bot.download_file(file_info.file_path)
            logger.info("Файл успешно скачан")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"data/photo_{timestamp}_{photo.file_id}.jpg"

            save_dir = os.path.dirname(save_path) or "."
            if not os.access(save_dir, os.W_OK):
                logger.error(f"Нет прав на запись в директорию: {save_dir}")
                await message.reply("Ошибка: Нет прав на запись в директорию.",
                                    reply_markup=kb.registred_user)
                return

            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file.read())

            if os.path.exists(save_path):
                logger.info(f"Фотография сохранена как {save_path}")
                await state.update_data(photo=save_path)
            else:
                logger.error("Файл не был сохранен")
                await message.reply("Файл не был сохранен.",
                                    reply_markup=kb.registred_user)
            user.get_user(message.from_user.id).change_photo(save_path)
        except Exception as e:
            logger.error(f"Ошибка при обработке фотографии: {str(e)}")
        if message.content_type != ContentType.PHOTO:
            await message.reply('Отправьте фото!')
            return
        await message.reply(
            text="Спасибо! Новое фото было сохранено!",
            reply_to_message_id=message.message_id,
            reply_markup=kb.registred_user
        )
        await state.clear()

    @router.message(F.text.contains('Посмотреть свою анкету'))
    async def show_anket(message: Message, state: FSMContext):
        us = user.get_user(message.from_user.id)
        await message.reply(text="Ваша анкета выглядит так:")
        if us:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=FSInputFile(us.photo),
                caption=f"{us.name}, {us.description}",
            )
    # тут будет бот присылать сообщение полной анкеты
