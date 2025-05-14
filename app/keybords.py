from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

otdaivincikBot = ReplyKeyboardMarkup(keyboard=
                                     [[types.KeyboardButton(text='Остановить создание анкеты')]])
registred_user = ReplyKeyboardMarkup(keyboard=
                                     [[types.KeyboardButton(text='Смотреть анкеты')],
                                      [types.KeyboardButton(text='Изменить имя')],
                                      [types.KeyboardButton(text='Изменить описание')],
                                      [types.KeyboardButton(text='Изменить список интересов')],
                                      [types.KeyboardButton(text='Поменять фогографию')],
                                      [types.KeyboardButton(text='Посмотреть свою анкету')]])
