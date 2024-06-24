from aiogram import Router, F
from aiogram.types import CallbackQuery
from create_bot import bot
from config import ADMINS


subscribe_router = Router()


@subscribe_router.callback_query(F.data == "subscribe")
async def subscribe_cmd(callback_query: CallbackQuery):
  if callback_query.message.from_user.username:
    await callback_query.message.delete()
    await callback_query.message.answer("Заявка отправлена. В ближайшее время с Вами свяжутся")
    
    for admin_id in ADMINS:
      await bot.send_message(
				admin_id,
				f"Пользователь @{callback_query.from_user.username} хотел бы записаться на тренировку",
			)
  else:
    await callback_query.message.answer("Ваш нужно создать никнейм в Telegram, чтобы позже с Вами мог связаться тренер")