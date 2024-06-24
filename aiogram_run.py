import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.trainings import trainings_router
from handlers.admin_cmds import admin_router
from handlers.menus import menu_router
from handlers.programs import program_router
from database.session import engine
from database.models import Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()
    
    dp.include_router(program_router)
    dp.include_router(menu_router)
    dp.include_router(start_router)
    dp.include_router(trainings_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())