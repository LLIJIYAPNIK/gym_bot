from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.inline.start import get_start_kb


start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()', reply_markup=get_start_kb())
