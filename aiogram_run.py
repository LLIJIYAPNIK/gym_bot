import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.trainings import trainings_router
from handlers.admin_cmds import admin_router
from handlers.menus import menu_router
from handlers.programs import program_router
from handlers.subscribe import subscribe_router
from database.session import engine
from database.models import Base
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from config import ADMINS


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
async def set_bot_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/faq", description="Помощь")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    
    admins_commands = [
        BotCommand(command="/add_muscle", description="Добавить упражнение"),
        BotCommand(command="/edit_muscle", description="Изменить упражнение"),
        BotCommand(command="/delete_muscle", description="Удалить упражнение"),
        BotCommand(command="/get_table", description="Получить структуру таблицы"),
        BotCommand(command="/send_document", description="Отправить документ пользователю"),
        BotCommand(command="/get_document", description="Получить документ"),
        BotCommand(command="/get_username", description="Получить никнейм пользователя"),
        BotCommand(command="/commands", description="Список команд и их использование")
    ]
    
    for admin_id in ADMINS:
        await bot.set_my_commands(admins_commands, scope=BotCommandScopeChat(chat_id=admin_id))
    


async def main():
    await create_tables()
    
    dp.include_router(start_router)
    dp.include_router(subscribe_router)
    dp.include_router(program_router)
    dp.include_router(menu_router)
    dp.include_router(trainings_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
