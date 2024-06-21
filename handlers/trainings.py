from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.start import get_start_kb
from keyboards.inline.training import get_training_kb


trainings_router = Router()

@trainings_router.callback_query(F.data == 'training')
async def cmd_training(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Выберете желаемую группу мышц', reply_markup=get_training_kb())
    

@trainings_router.callback_query(F.data == 'back_to_start')
async def cmd_back_to_start(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Запуск сообщения по команде /start используя фильтр CommandStart()', reply_markup=get_start_kb())
