from additionally import Singleton
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardMarkup,
                           KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.filters import Command, CommandStart
import random
import app.keyboards as kb

router = Router()
s = Singleton()


# Хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id not in s.users.keys():
        s.users[message.from_user.id] = [[0, 0, 0, 0], [[' '] * 3 for _ in range(3)],
                                         [str(i) + ',' + str(j) for i in range(0, 3) for j in range(0, 3)]]
    await message.answer(f'Привет, '                        
                         f'{('НОВИЧОК' if s.users[message.from_user.id][0][3] <= 5 else '')}'
                         f'{' ХОРОШИЙ ИГРОК' if (5 < s.users[message.from_user.id][0][3]) <=10 else ''}'
                         f'{'ПЕРВОКЛАССНЫЙ ИГРОК' if (10 < s.users[message.from_user.id][0][3] <= 100) else ''}'
                         f'{'МАСТЕР' if 100 < s.users[message.from_user.id][0][3] <= 1000 else ''}'
                         f'{'СУПЕР МАСТЕР' if s.users[message.from_user.id][0][3] > 1000 else ''}'
                         f' {message.from_user.first_name} {message.from_user.last_name}!'
                         f' Сыграем в Крестики-Нолики?', reply_markup=kb.main)


@router.message(F.text == 'Правила')
async def rules_game(message: Message):
    await message.answer(text='Ваша задача - проиграть боту в классические Крестики-Нолики '
                              'Игроки по очереди ставят на свободные клетки поля 3×3 знаки/ '
                              'Oдин всегда "X", другой всегда "0".\n'
                              ' Первый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали '
                              'или большой диагонали, ПРОИГРЫВАЕТ. \n'
                              '\n'
                              'Если игроки заполнили все '
                              '9 ячеек и оказалось, что ни в одной вертикали, горизонтали или'
                              ' большой диагонали нет трёх одинаковых знаков, партия считается'
                              ' закончившейся в ничью. Так же если и у вас и у бота есть три знака'
                              'в ряд или по диагонали, то это тоже ничья. Первый ход делает игрок, ставящий крестики.\n'
                              ''
                              '\n'
                              'МАСТЕРСТВО В ИГРЕ подразделяется на 5 уровней: \n'
                              '\nНОВИЧОК - до 5 побед\n'
                              '\nХОРОШИЙ ИГРОК - до 10 побед\n'
                              '\nПЕРВОКЛАССНЫЙ ИГРОК- больше 10 побед\n'
                              '\nМАСТЕР - больше 100 побед\n'
                              '\nСУПЕР МАСТЕР - больше 1000 побед'
                         )


@router.message(F.text == 'Новая игра')
async def new_game(message: Message):
    if message.from_user.id not in s.users.keys():
        s.users[message.from_user.id] = [[0, 0, 0, 0], [[' '] * 3 for _ in range(3)],
                                         [str(i) + ',' + str(j) for i in range(0, 3) for j in range(0, 3)]]
    else:
        s.users[message.from_user.id][1] = [['  '] * 3 for _ in range(3)]
        s.users[message.from_user.id][2] = [str(i) + ',' + str(j) for i in range(0, 3) for j in range(0, 3)]
    s.users[message.from_user.id][0][0] = s.users[message.from_user.id][0][0] + 1
    await message.answer('Игра', reply_markup=kb.gameKeyboard)


@router.message(F.text == 'Достижения')
async def result_game(message: Message):
    q = s.users[message.from_user.id][0][1]
    w = s.users[message.from_user.id][0][2]
    e = s.users[message.from_user.id][0][3]
    ng = (s.users[message.from_user.id][0][0] - q - w - e)
    await message.answer(text=f'{message.from_user.first_name} {message.from_user.last_name} \n'
                              f'Вы - {'НОВИЧОК' if s.users[message.from_user.id][0][3] <= 5 else ''}'
                              f'{' ХОРОШИЙ ИГРОК' if (5 < s.users[message.from_user.id][0][3]) <= 10 else ''}'
                              f'{'ПЕРВОКЛАССНЫЙ ИГРОК' if (10 < s.users[message.from_user.id][0][3] <= 100) else ''}'
                              f'{'МАСТЕР' if 100 < s.users[message.from_user.id][0][3] <= 1000 else ''}'
                              f'{'СУПЕР МАСТЕР' if s.users[message.from_user.id][0][3] > 1000 else ''}'
                              f'\nВаши результаты: \n'
                              f'Всего игр: {s.users[message.from_user.id][0][0]} \n'
                              f'Поражения: {s.users[message.from_user.id][0][1]} \n'
                              f'Ничьи: {s.users[message.from_user.id][0][2]} \n'
                              f'Победы: {s.users[message.from_user.id][0][3]} \n'
                              f'Незавершенных игр: {ng}')



@router.callback_query(F.data == '0,0')
async def step1(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][0][0] == '  ':
        s.users[callback.from_user.id][1][0][0] = 'X'
        s.users[callback.from_user.id][2].remove('0,0')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ходите',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                    pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                    pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                    pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                    pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                    pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                    pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                    pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
           # await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '0,1')
async def step2(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][0][1] == '  ':
        s.users[callback.from_user.id][1][0][1] = 'X'
        s.users[callback.from_user.id][2].remove('0,1')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ваша очередь ходить!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][
                                                                                  1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
           # await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '0,2')
async def step3(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][0][2] == '  ':
        s.users[callback.from_user.id][1][0][2] = 'X'
        s.users[callback.from_user.id][2].remove('0,2')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ходите',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли, {callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '1,0')
async def step4(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][1][0] == '  ':
        s.users[callback.from_user.id][1][1][0] = 'X'
        s.users[callback.from_user.id][2].remove('1,0')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ходите же!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
           # await callback.message.delete()
            await callback.message.answer(f'Вы победили {callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '1,1')
async def step5(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][1][1] == '  ':
        s.users[callback.from_user.id][1][1][1] = 'X'
        s.users[callback.from_user.id][2].remove('1,1')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ходите! Ходите!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!', reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                                                   s.users[
                                                                                                       callback.from_user.id][
                                                                                                       1]))


@router.callback_query(F.data == '1,2')
async def step6(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][1][2] == '  ':
        s.users[callback.from_user.id][1][1][2] = 'X'
        s.users[callback.from_user.id][2].remove('1,2')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ходите',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '2,0')
async def step7(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][2][0] == '  ':
        s.users[callback.from_user.id][1][2][0] = 'X'
        s.users[callback.from_user.id][2].remove('2,0')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Теперь Вы',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '2,1')
async def step8(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][2][1] == '  ':
        s.users[callback.from_user.id][1][2][1] = 'X'
        s.users[callback.from_user.id][2].remove('2,1')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ходите',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            # await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            # await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            # await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))


@router.callback_query(F.data == '2,2')
async def step9(callback: CallbackQuery):
    if s.users[callback.from_user.id][1][2][2] == '  ':
        s.users[callback.from_user.id][1][2][2] = 'X'
        s.users[callback.from_user.id][2].remove('2,2')

        if s.users[callback.from_user.id][2]:
            k = random.choice(s.users[callback.from_user.id][2]).split(',')
            x, y = int(k[0]), int(k[1])
            s.users[callback.from_user.id][1][x][y] = 'O'
            s.users[callback.from_user.id][2].remove(str(x) + ',' + str(y))
            await callback.message.delete()
            await callback.message.answer(f'Ваш ход',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        pf = s.users[callback.from_user.id][1]
        if ((pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
             pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
             pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
             pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
             pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
             pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
             pf[2][0] == pf[1][1] == pf[0][2] == 'X') and (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                                                           pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                                                           pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                                                           pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                                                           pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                                                           pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                                                           pf[2][0] == pf[1][1] == pf[0][2] == 'O')) or (
                s.users[callback.from_user.id][2] == [] and (
                not (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
                     pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
                     pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
                     pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
                     pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
                     pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
                     pf[2][0] == pf[1][1] == pf[0][2] == 'X') and not (
                pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
                pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
                pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
                pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
                pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
                pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
                pf[2][0] == pf[1][1] == pf[0][2] == 'O'))):
            s.users[callback.from_user.id][0][2] = s.users[callback.from_user.id][0][2] + 1
            #await callback.message.delete()
            await callback.message.answer(f'НИЧЬЯ !!! Спасибо за игру, '
                                          f'{callback.from_user.first_name} {callback.from_user.last_name}!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'X' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'X' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'X' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'X' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'X' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'X' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'X'):
            s.users[callback.from_user.id][0][1] = s.users[callback.from_user.id][0][1] + 1
            #await callback.message.delete()
            await callback.message.answer(
                f'Вы проиграли,{callback.from_user.first_name} {callback.from_user.last_name}!'
                f'Спасибо за игру!',
                reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                    s.users[callback.from_user.id][1]))
        elif (pf[0][0] == pf[0][1] == pf[0][2] == 'O' or
              pf[1][0] == pf[1][1] == pf[1][2] == 'O' or
              pf[2][0] == pf[2][1] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][0] == pf[2][0] == 'O' or
              pf[0][1] == pf[1][1] == pf[2][1] == 'O' or
              pf[0][2] == pf[1][2] == pf[2][2] == 'O' or
              pf[0][0] == pf[1][1] == pf[2][2] == 'O' or
              pf[2][0] == pf[1][1] == pf[0][2] == 'O'):
            s.users[callback.from_user.id][0][3] = s.users[callback.from_user.id][0][3] + 1
            #await callback.message.delete()
            await callback.message.answer(f'Вы победили,{callback.from_user.first_name} '
                                          f'{callback.from_user.last_name}!'
                                          f'Спасибо за игру!',
                                          reply_markup=kb.get_inline_keyboard(kb.gameKeyboard,
                                                                              s.users[callback.from_user.id][1]))
