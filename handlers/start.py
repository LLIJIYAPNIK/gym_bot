from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.inline.start import get_start_kb
from aiogram.fsm.context import FSMContext


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать! Выберите интересующий раздел, чтобы начать",
        reply_markup=get_start_kb(),
    )


@start_router.callback_query(F.data == "back_to_start")
async def cmd_back_to_start(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Добро пожаловать! Выберите интересующий раздел, чтобы начать",
        reply_markup=get_start_kb(),
    )
