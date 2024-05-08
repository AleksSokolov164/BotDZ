from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

import app.keyboards as kb

router = Router()

# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.username}")

# Хэндлер на команду /help
@router.message(Command("game"))
async def cmd_game(message: Message):
    await message.answer("Новая игра", reply_markup=kb.main)

@router.message(F.text == 'Новая игра')
async def catalog(message: Message):
    await message.answer('Хорошо', reply_markup=kb.catalog)

# Хэндлер эхо
@router.message()
async def echo(message: Message):
    await message.answer(text=message.text)

