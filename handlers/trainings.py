from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaVideo
from database.models import Training
from database.session import SessionLocal
from keyboards.inline.start import get_start_kb
from aiogram.utils.chat_action import ChatActionSender
from database.crud import DatabaseManager
from keyboards.inline.training import MuscleKeyboard
import json
from create_bot import bot


trainings_router = Router()


@trainings_router.callback_query(F.data == 'back_to_training')
async def cmd_back_to_training(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Выберите группу мышц, чтобы продолжить', reply_markup=await MuscleKeyboard().get_main_keyboard())


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
    await callback_query.message.edit_text('Выберите группу мышц, чтобы продолжить', reply_markup=await MuscleKeyboard().get_main_keyboard())


@trainings_router.callback_query(lambda c: True)
async def process_callback_data(callback_query: CallbackQuery):
    data = callback_query.data
    if str(data).isdigit():
        muscles = await get_muscles()
        # muscles_types = await get_muscle_types(data)
        dictioary = json.loads(open('translations.json', 'r', encoding='utf-8').read())
        print(dictioary)
        
        key = get_key_by_value(dictioary, data)
        if key in muscles:
            await callback_query.message.edit_text('Выберите группу мышц, чтобы увидеть доступные упражнения', reply_markup= await MuscleKeyboard().get_sub_keyboard(key))
        else:
            video_ids = set(await DatabaseManager(Training, SessionLocal).get_by_condition(condition=(Training.muscle_type == key), quantity=True, select_this=Training.video_id))
            
            if video_ids:
                async with ChatActionSender.upload_video(bot=bot, chat_id=callback_query.message.chat.id):
                    await callback_query.message.delete()
                    await bot.send_media_group(callback_query.message.chat.id, [InputMediaVideo(type="video", media=video_id) for video_id in video_ids], protect_content=True)
            else:
                await callback_query.message.delete()
                await callback_query.message.edit_text('Нет видео для этого упражнения', reply_markup=await get_start_kb())
            