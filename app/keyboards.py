from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Правила'),
                                      KeyboardButton(text='Новая игра'),
                                      KeyboardButton(text='Достижения')],
                                    ],
                           input_field_placeholder='Меню')

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='1'),
     InlineKeyboardButton(text='2', callback_data='1'),
     InlineKeyboardButton(text='3', callback_data='1')],
    [InlineKeyboardButton(text='4', callback_data='1'),
     InlineKeyboardButton(text='5', callback_data='1'),
     InlineKeyboardButton(text='6', callback_data='1')],
    [InlineKeyboardButton(text='7', callback_data='1'),
     InlineKeyboardButton(text='8', callback_data='1'),
     InlineKeyboardButton(text='9', callback_data='1')],
]
)
