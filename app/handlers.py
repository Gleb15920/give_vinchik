from aiogram.enums import ParseMode, ContentType
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, types, F
import give_vinchik.app.keybords as kb

router = Router()

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
        photo_data = message.photo[-1] #сохранение присланной фотки
        await message.reply('Фотография добавлена в анкету!')

    @router.message(F.content_type != ContentType.PHOTO)
    async def handle_non_photo(message: types.Message):
        await message.reply("Это не фото")

@router.message(F.text.lower() == "2")
async def two_answ(message: types.Message):
    await message.answer("Пришлите описание анкеты")

@router.message(F.text.lower() == "3")
async def three_answ(message: types.Message):
    await message.answer("Напишите искомые интересы")
