from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.inline.start import get_start_kb
from aiogram.fsm.context import FSMContext
from database.crud import DatabaseManager
from database.models import User
from database.session import SessionLocal


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Сейчас начнём...", reply_markup=ReplyKeyboardRemove())
    if int(message.from_user.id) not in [int(await DatabaseManager(User, SessionLocal).get_by_condition(condition=(User.user_id == int(message.from_user.id)), select_this=User.user_id))]:
        await DatabaseManager(User, SessionLocal).add(
            user_id = message.from_user.id,
            status = "free"
        )
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
    
    
@start_router.message(F.text == "faq")
async def cmd_faq(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Сейчас начнём...", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Что может этот бот?\nБот может отправлять видео с правильной техникой, доступны программы тренировок и готовые меню. Бот даёт возможность оставить заявку на получение персональной программы или меню. Для этого нужно заполнить анкету. В течение некоторого времени бот отправит Вам документы. Также можно оставить заявку на тренировку.\nЯ заполнял анкету, но передумал, как можно выйти? Введите любую команду и Вы автоматически вернетесь в главное меню.\nЧто нужно для корректной работы бота? У вас должен быть никнейм в Telegram, чтобы в случае чего с Вами мог связаться тренер.",
        reply_markup=ReplyKeyboardRemove()
    )
    