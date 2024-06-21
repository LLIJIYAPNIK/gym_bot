import asyncio
from aiogram import Bot, Dispatcher
from create_bot import create_bot

# Создаем бота и диспетчер
bot, dp = create_bot()

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())