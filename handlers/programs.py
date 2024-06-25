import re
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InputMediaDocument,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from database.models import Program, Questionnaire
from database.session import SessionLocal
from aiogram.utils.chat_action import ChatActionSender
from database.crud import DatabaseManager
from create_bot import bot
from keyboards.inline.programs import (
    get_main_program_train_kb,
    get_ready_programs_trains_kb,
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import ADMINS


program_router = Router()


@program_router.callback_query(F.data == "program")
async def cmd_programs(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите, чтобы продолжить", reply_markup=get_main_program_train_kb()
    )


@program_router.callback_query(F.data == "back_to_program")
async def cmd_back_to_program(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите, чтобы продолжить", reply_markup=get_main_program_train_kb()
    )


@program_router.callback_query(F.data == "ready_trains")
async def cmd_ready_programs(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите, чтобы продолжить", reply_markup=get_ready_programs_trains_kb()
    )


@program_router.callback_query(F.data == "pr1")
async def cmd_pr1(callback_query: CallbackQuery):
    await DatabaseManager(Program, SessionLocal).add(
        user_id=int(callback_query.from_user.id),
        type_training="Программа_1",
        file_id="BQACAgIAAxkBAAIEK2Z5iomgtSshjBeKV8q7o8qX32Q2AALATgACnyHJS9BF0BvipTWONQQ"
    )
    
    async with ChatActionSender.upload_document(bot=bot, chat_id=callback_query.message.chat.id):
        await callback_query.message.delete()
        try:
            await bot.send_document(
                chat_id=callback_query.message.chat.id,
                document="BQACAgIAAxkBAAIEK2Z5iomgtSshjBeKV8q7o8qX32Q2AALATgACnyHJS9BF0BvipTWONQQ",
                protect_content=True
            )
        except Exception as e:
            await callback_query.message.edit_text(
                "Документ не найден. Попробуйте позже"
            )


@program_router.callback_query(F.data == "pr2")
async def cmd_pr1(callback_query: CallbackQuery):
    await DatabaseManager(Program, SessionLocal).add(
        user_id=int(callback_query.from_user.id),
        type_training="Программа_2",
        file_id="BQACAgIAAxkBAAIELWZ5iq2BfrtTLuZarz3sQ0OSRdtgAALCTgACnyHJS91GmSmKz8mZNQQ"
    )
    
    async with ChatActionSender.upload_document(
        bot=bot, chat_id=callback_query.message.chat.id
    ):
        await callback_query.message.delete()
        try:
            await bot.send_document(
                chat_id=callback_query.message.chat.id,
                document="BQACAgIAAxkBAAIELWZ5iq2BfrtTLuZarz3sQ0OSRdtgAALCTgACnyHJS91GmSmKz8mZNQQ",
                protect_content=True
            )
        except:
            await callback_query.message.edit_text(
                "Документ не найден. Попробуйте позже"
            )


@program_router.callback_query(F.data == "pr3")
async def cmd_pr1(callback_query: CallbackQuery):
    await DatabaseManager(Program, SessionLocal).add(
        user_id=int(callback_query.from_user.id),
        type_training="Программа_3",
        file_id="BQACAgIAAxkBAAIEL2Z5ir0pdWHfhuCfisYbgUpMl0mwAAKySgACnyHRS0X7xPN7xGMkNQQ"
    )
    
    async with ChatActionSender.upload_document(
        bot=bot, chat_id=callback_query.message.chat.id
    ):
        await callback_query.message.delete()
        try:
            await bot.send_document(
                chat_id=callback_query.message.chat.id,
                document="BQACAgIAAxkBAAIEL2Z5ir0pdWHfhuCfisYbgUpMl0mwAAKySgACnyHRS0X7xPN7xGMkNQQ",
                protect_content=True
            )
        except:
            await callback_query.message.edit_text(
                "Документ не найден. Попробуйте позже"
            )


class Form(StatesGroup):
    physical_training = State()
    purpose = State()
    preference = State()
    days = State()
    time = State()
    health = State()
    equipment = State()
    experience = State()
    nutrition = State()
    sleeping = State()


@program_router.callback_query(F.data == "personal_trains")
async def cmd_personal_program(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user.username:
        await state.set_state(Form.physical_training)

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Начальный")],
                [KeyboardButton(text="Средний")],
                [KeyboardButton(text="Продвинутый")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        await callback_query.message.delete()
        await callback_query.message.answer(
            "Чтобы получить программу тренировок, нужно заполнить анкету. Давайте начнём. Укажите вашу физическую подготовку: ",
            reply_markup=keyboard,
        )
    else:
        await callback_query.message.answer(
            "Ваш нужно создать никнейм в Telegram, чтобы позже с Вами мог связаться тренер"
        )


@program_router.message(Form.physical_training)
async def get_purpose(message: Message, state: FSMContext):
    if message.text.lower() in ["начальный", "средний", "продвинутый"]:
        if message.text.lower() in ["начальный", "средний", "продвинутый"]:
            await state.update_data(physical_training=message.text)
            await state.set_state(Form.purpose)

            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Набор мышечной массы")],
                    [KeyboardButton(text="Снижение веса")],
                    [KeyboardButton(text="Улучшение физической формы")],
                    [KeyboardButton(text="Улучшение силовых показателей")],
                    [KeyboardButton(text="Поддержание общего состояния здоровья")],
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            )

            await message.answer("Ваша цель: ", reply_markup=keyboard)
        else:
            await message.answer(
                "Вы ввели некорректные данные. Введите вашу физическую подготовку (используйте кнопки): "
            ) 


@program_router.message(Form.purpose)
async def get_physical_training(message: Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await state.set_state(Form.preference)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кардио")],
            [KeyboardButton(text="Силовые тренировки")],
            [KeyboardButton(text="Групповые занятия")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer("Предпочтительный вид тренировок: ", reply_markup=keyboard)


@program_router.message(Form.preference)
async def get_preference(message: Message, state: FSMContext):
    if message.text.lower() in ["кардио", "силовые тренировки", "групповые занятия"]:
        await state.update_data(preference=message.text)
        await state.set_state(Form.days)

        await message.answer(
            "Количество тренировок в неделю: "
        )
    else:
        await message.answer(
            "Вы ввели некорректные данные. Введите предпочтительный вид тренировок: "
        )


@program_router.message(Form.days)
async def get_days(message: Message, state: FSMContext):
    if 1 <= int(message.text) <= 7:
        await state.update_data(days=message.text)
        await state.set_state(Form.time)

        await message.answer(
            "В какое время Вы хотите заниматься (начало-конец): "
        )
    else:
        await message.answer(
            "Вы ввели некорректные данные. Введите количество тренировок в неделю (1-7): "
        )


@program_router.message(Form.time)
async def get_time(message: Message, state: FSMContext):
    if is_valid_time_format(message.text):
        await state.update_data(time=message.text)
        await state.set_state(Form.health)

        await message.answer(
            "Есть ли какие-то заболевания или травмы? Рекомендации врачей? "
        )
    else:
        await message.answer(
            "Вы ввели некорректные данные. Введите время (начало-конец): "
        )


@program_router.message(Form.health)
async def get_health(message: Message, state: FSMContext):
    await state.update_data(health=message.text)
    await state.set_state(Form.equipment)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В зале")], [KeyboardButton(text="Дома")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer("Где Вы тренируетесь?", reply_markup=keyboard)


@program_router.message(Form.equipment)
async def get_equipment(message: Message, state: FSMContext):
    if message.text.lower() in ["в зале", "дома"]:
        await state.update_data(equipment=message.text)
        await state.set_state(Form.experience)

        await message.answer(
            "Был ли опыт до этого (Прошлые программы тренировок, результаты прошлых тренировок)"
        )
    else:
        await message.answer(
            "Вы ввели некорректные данные. Введите где Вы тренируетесь (В зале/Дома): "
        )


@program_router.message(Form.experience)
async def get_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Form.nutrition)

    await message.answer(
        "Приём пиши до и после тренировки"
    )


@program_router.message(Form.nutrition)
async def get_nutrition(message: Message, state: FSMContext):
    await state.update_data(nutrition=message.text)
    await state.set_state(Form.sleeping)

    await message.answer("Сколько часов Вы спите")


@program_router.message(Form.sleeping)
async def get_sleeping(message: Message, state: FSMContext):
    if int(message.text) > 0:
        await state.update_data(sleeping=message.text)
        data = await state.get_data()
        await state.clear()

        formatted_text = []

        russian_keys = {
            "physical_training": "Уровень физической подготовки",
            "purpose": "Цель",
            "preference": "Предпочтительный вид тренировки",
            "days": "Количество тренировок в неделю",
            "time": "Время тренировки",
            "health": "Здоровье",
            "equipment": "Место тренировок",
            "experience": "Опыт до этого",
            "nutrition": "Приём пиши до и после тренировки",
            "sleeping": "Сон",
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
        await message.answer(
            "Тренер получил Вашу анкету и работает над Вашей программой"
        )
        await DatabaseManager(Program, SessionLocal).add(
            user_id=int(message.from_user.id),
            type_training="Персональная программа",
            file_id=0
        )
        await DatabaseManager(Questionnaire, SessionLocal).add(
            user_id=int(message.from_user.id),
            type_questionnaire="Программа тренировок",
            questionnaire_id=sent_message.message_id,
        )

        for admin_id in ADMINS:
            await bot.forward_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=sent_message.message_id,
            )
    else:
        await message.answer("Вы ввели некорректные данные. Сколько часов Вы спите? ")


def is_valid_time_format(time_str):
    # Проверяем, что строка соответствует формату hh:mm-hh:mm или h:mm-h:mm
    pattern = r"^(\d{1,2}:\d{2})-(\d{1,2}:\d{2})$"
    if not re.match(pattern, time_str):
        return False

    # Разделяем строку на части
    parts = time_str.split("-")
    start_time = parts[0].split(":")
    end_time = parts[1].split(":")

    # Проверяем, что часы и минуты находятся в допустимых диапазонах
    try:
        start_h, start_m = int(start_time[0]), int(start_time[1])
        end_h, end_m = int(end_time[0]), int(end_time[1])
    except ValueError:
        return False

    if not (
        0 <= start_h < 24 and 0 <= start_m < 60 and 0 <= end_h < 24 and 0 <= end_m < 60
    ):
        return False

    # Проверяем, что время начала не больше времени окончания
    if start_h > end_h or (start_h == end_h and start_m >= end_m):
        return False

    return True
