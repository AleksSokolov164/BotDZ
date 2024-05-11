from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Правила'),
                                      KeyboardButton(text='---------Новая игра---------'),
                                      KeyboardButton(text='Достижения')],
                                    ],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню')

gameKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f' ', callback_data='0,0'),
     InlineKeyboardButton(text=f' ', callback_data='0,1'),
     InlineKeyboardButton(text=f' ', callback_data='0,2')],
    [InlineKeyboardButton(text=f' ', callback_data='1,0'),
     InlineKeyboardButton(text=f' ', callback_data='1,1'),
     InlineKeyboardButton(text=f' ', callback_data='1,2')],
    [InlineKeyboardButton(text=f' ', callback_data='2,0'),
     InlineKeyboardButton(text=f' ', callback_data='2,1'),
     InlineKeyboardButton(text=f' ', callback_data='2,2')],
]
)

def get_inline_keyboard(gameKeyboard, l):
    gameKeyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{l[0][0]}', callback_data='0,0'),
         InlineKeyboardButton(text=f'{l[0][1]}', callback_data='0,1'),
         InlineKeyboardButton(text=f'{l[0][2]}', callback_data='0,2')],
        [InlineKeyboardButton(text=f'{l[1][0]}', callback_data='1,0'),
         InlineKeyboardButton(text=f'{l[1][1]}', callback_data='1,1'),
         InlineKeyboardButton(text=f'{l[1][2]}', callback_data='1,2')],
        [InlineKeyboardButton(text=f'{l[2][0]}', callback_data='2,0'),
         InlineKeyboardButton(text=f'{l[2][1]}', callback_data='2,1'),
         InlineKeyboardButton(text=f'{l[2][2]}', callback_data='2,2')]])
    return gameKeyboard