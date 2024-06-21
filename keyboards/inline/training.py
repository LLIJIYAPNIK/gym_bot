from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_training_kb() -> InlineKeyboardMarkup:
  kb_list = [
		[InlineKeyboardButton(text="Спина", callback_data="back_training")],
		[InlineKeyboardButton(text="Грудь", callback_data="chest_training")],
		[InlineKeyboardButton(text="Плечи", callback_data="shoulders_training")],
		[InlineKeyboardButton(text="Ноги", callback_data="legs_training")],
		[InlineKeyboardButton(text="Руки", callback_data="arms_training")],
		[InlineKeyboardButton(text="Пресс", callback_data="press_training")],
		[InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
	]
  
  return InlineKeyboardMarkup(inline_keyboard=kb_list)