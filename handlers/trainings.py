from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import Training
from database.session import SessionLocal
from keyboards.inline.start import get_start_kb
from keyboards.inline.training import get_training_kb
from database.crud import DatabaseManager
from keyboards.inline.training import MuscleKeyboard
import json
from create_bot import bot


trainings_router = Router()
video_router = Router()

@trainings_router.callback_query(F.data == 'back_to_start')
async def cmd_back_to_start(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Запуск сообщения по команде /start используя фильтр CommandStart()', reply_markup=get_start_kb())
    

@trainings_router.callback_query(F.data == 'back_to_training')
async def cmd_back_to_training(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Выберете желаемую группу мышц', reply_markup=await MuscleKeyboard().get_main_keyboard())


def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if int(val) == int(value):
            return key
    return None  # Возвращаем None, если значение не найдено


async def get_muscles():
    return set(await DatabaseManager(Training, SessionLocal).get_by_condition(condition=(Training.muscle != None), quantity=True, select_this=Training.muscle))


async def get_muscle_types(muscle):
    return set(await DatabaseManager(Training, SessionLocal).get_by_condition(condition=(Training.muscle == muscle), quantity=True, select_this=Training.muscle_type))


@trainings_router.callback_query(F.data == 'training')
async def cmd_training(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Выберете желаемую группу мышц', reply_markup=await MuscleKeyboard().get_main_keyboard())


@trainings_router.callback_query(lambda c: True)
async def process_callback_data(callback_query: CallbackQuery):
    data = callback_query.data
    
    muscles = await get_muscles()
    muscles_types = await get_muscle_types(data)
    dictioary = json.loads(open('translations.json', 'r', encoding='utf-8').read())
    print(dictioary)
    
    key = get_key_by_value(dictioary, data)
    if key in muscles:
        print(key)
        await callback_query.message.edit_text('Выберете желаемую группу мышц:', reply_markup= await MuscleKeyboard().get_sub_keyboard(key))
    else:
        await callback_query.message.edit_text("Должно высылаться видео")
    
    