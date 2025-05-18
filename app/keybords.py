from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

otdaivincikBot = ReplyKeyboardMarkup(keyboard=
                                     [[types.KeyboardButton(text='Остановить создание анкеты')]])
registred_user = ReplyKeyboardMarkup(keyboard=
                                     [[types.KeyboardButton(text='Смотреть анкеты')],
                                      [types.KeyboardButton(text='Изменить имя'),
                                       types.KeyboardButton(text='Изменить описание')],
                                      [types.KeyboardButton(text='Изменить список интересов'),
                                       types.KeyboardButton(text='Поменять фотографию')],
                                      [types.KeyboardButton(text='Посмотреть свою анкету')],
                                      [types.KeyboardButton(text='/start')]
                                      ])
change = ReplyKeyboardMarkup(keyboard=
                             [[types.KeyboardButton(text='Отмена')]])

lenta = ReplyKeyboardMarkup(keyboard=
                            [[types.KeyboardButton(text='👍'), types.KeyboardButton(text='👎'),
                              types.KeyboardButton(text='⛔️')]])
