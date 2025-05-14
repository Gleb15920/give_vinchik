from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram import Router, types, F
import give_vinchik.app.keybords as kb

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