import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from additionally import Singleton
from secrets import bot_token
import csv

from app.handlers import router, s

# Объект бота
bot = Bot(bot_token)
# Диспетчер
dp = Dispatcher()
dp.include_router(router)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


# Inline keyboard


if __name__ == "__main__":
    try:
        with open("saved_users.txt", "r") as f:
            w = csv.DictReader(f, ["id", "game", "over", "draw", "won"])
            for i in w:
                if i["id"] == "id":
                    continue
                else:
                    id = int(i["id"])
                    game = int(i["game"])
                    over = int(i["over"])
                    draw = int(i["draw"])
                    won = int(i["won"])
                    s.users[id] = [[game, won, draw, over], [['  '] * 3 for _ in range(3)],
                                   [str(i) + ',' + str(j) for i in range(0, 3) for j in range(0, 3)]]
        asyncio.run(main())
    except KeyboardInterrupt:
        with open("saved_users.txt", "w", newline="") as v:
            w = csv.DictWriter(v, ["id", "game", "over", "draw", "won"])
            w.writeheader()
            for key, value in s.users.items():
                data_user = dict()
                data_user["id"] = key
                data_user["game"] = s.users[key][0][0]
                data_user["won"] = s.users[key][0][1]
                data_user["draw"] = s.users[key][0][2]
                data_user["over"] = s.users[key][0][3]
                w.writerow(data_user)
        print('Бот выключен')
