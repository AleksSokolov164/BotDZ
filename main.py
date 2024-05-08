import asyncio
from aiogram import Bot, Dispatcher
from secrets import bot_token

from app.handlers import router


# Запуск процесса поллинга новых апдейтов
async def main():
    # Объект бота
    bot = Bot(bot_token)
    # Диспетчер
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
