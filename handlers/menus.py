from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InputMediaDocument,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from database.models import Menu, Questionnaire
from database.session import SessionLocal
from aiogram.utils.chat_action import ChatActionSender
from database.crud import DatabaseManager
from create_bot import bot
from keyboards.inline.menus import get_main_promgrams_kb, get_ready_programs_kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import ADMINS


menu_router = Router()


@menu_router.callback_query(F.data == "menus")
async def cmd_programs(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите, чтобы продолжить", reply_markup=get_main_promgrams_kb()
    )


@menu_router.callback_query(F.data == "ready_programs")
async def cmd_ready_programs(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите меню, чтобы продолжить", reply_markup=get_ready_programs_kb()
    )


@menu_router.callback_query(F.data == "weight_loss")
async def cmd_weight_loss(callback_query: CallbackQuery):
    await DatabaseManager(Menu, SessionLocal).add(
        user_id=int(callback_query.from_user.id),
        type_menu="Похудение",
        file_id="file_id",
    )

    async with ChatActionSender.upload_document(
        bot=bot, chat_id=callback_query.message.chat.id
    ):
        await callback_query.message.delete()
        await bot.send_document(
            callback_query.message.chat.id,
            InputMediaDocument(type="document", media=""),
        )


@menu_router.callback_query(F.data == "muscle_gain")
async def cmd_weight_loss(callback_query: CallbackQuery):
    await DatabaseManager(Menu, SessionLocal).add(
        user_id=int(callback_query.from_user.id),
        type_menu="Набор массы",
        file_id="file_id",
    )

    async with ChatActionSender.upload_document(
        bot=bot, chat_id=callback_query.message.chat.id
    ):
        await callback_query.message.delete()
        await bot.send_document(
            callback_query.message.chat.id,
            InputMediaDocument(type="document", media=""),
        )


@menu_router.callback_query(F.data == "form_support")
async def cmd_weight_loss(callback_query: CallbackQuery):
    await DatabaseManager(Menu, SessionLocal).add(
        user_id=int(callback_query.from_user.id),
        type_menu="Поддержание формы",
        file_id="file_id",
    )

    async with ChatActionSender.upload_document(
        bot=bot, chat_id=callback_query.message.chat.id
    ):
        await callback_query.message.delete()
        await bot.send_document(
            callback_query.message.chat.id,
            InputMediaDocument(type="document", media=""),
        )


class FormMenu(StatesGroup):
    age = State()
    sex = State()
    activity = State()
    purpose = State()
    limit = State()
    medicine = State()


@menu_router.callback_query(F.data == "personal_program")
async def cmd_personal_program(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.username:
        await state.set_state(FormMenu.age)
        await callback_query.message.edit_text(
            "Для получения персонального меню нужно заполнить анкету. Давайте начнём. Введите ваш возраст: "
        )
    else:
        await callback_query.message.answer(
            "Ваш нужно создать никнейм в Telegram, чтобы позже с Вами мог связаться тренер"
        )


@menu_router.message(FormMenu.age)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(FormMenu.sex)

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мужской")],
                [KeyboardButton(text="Женский")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        await message.answer("Ваш пол: ", reply_markup=keyboard)
    else:
        await message.answer(
            "Вы ввели некорректные данные. Введите ваш возраст (число): "
        )


@menu_router.message(FormMenu.sex)
async def get_sex(message: Message, state: FSMContext):
    if message.text.lower() in ["мужской", "женской"]:
        await state.update_data(sex=message.text)
        await state.set_state(FormMenu.activity)
        await message.answer(
            "Ваш уровень активности: ", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Вы ввели некорректные данные. Введите ваш пол (Используйте кнопки): "
        )


@menu_router.message(FormMenu.activity)
async def get_activity(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await state.set_state(FormMenu.purpose)
    await message.answer("Ваша цель: ")


@menu_router.message(FormMenu.purpose)
async def get_purpose(message: Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await state.set_state(FormMenu.limit)
    await message.answer("Ваши ограничения: ")


@menu_router.message(FormMenu.limit)
async def get_limit(message: Message, state: FSMContext):
    await state.update_data(limit=message.text)
    await state.set_state(FormMenu.medicine)
    await message.answer(
        "Есть ли у вас аллергические реакции или хронические заболевания? "
    )


@menu_router.message(FormMenu.medicine)
async def get_medicine(message: Message, state: FSMContext):
    await state.update_data(medicine=message.text)
    data = await state.get_data()
    await state.clear()

    formatted_text = []

    russian_keys = {
        "age": "Возраст",
        "sex": "Пол",
        "activity": "Уровень активности",
        "purpose": "Цель",
        "limit": "Ограничения",
        "medicine": "Заболевания",
    }

    [
        formatted_text.append(f"{russian_keys[str(key)]}: {value}")
        for key, value in data.items()
    ]

    sent_message = await message.answer(
        "Ваша анкета: \n"
        + "\n".join(formatted_text)
        + f"\nНик в Telegram: @{message.chat.username}"
    )
    await message.answer("Тренер получил Вашу анкету и работает над Вашим меню")
    await DatabaseManager(Menu, SessionLocal).add(
        user_id=int(message.from_user.id), type_menu="Персональное меню", file_id="-"
    )
    await DatabaseManager(Questionnaire, SessionLocal).add(
        user_id=int(message.from_user.id),
        type_questionnaire="Персональное меню",
        questionnaire_id=sent_message.message_id,
    )

    for admin_id in ADMINS:
        await bot.forward_message(
            chat_id=admin_id,
            from_chat_id=message.chat.id,
            message_id=sent_message.message_id,
        )
