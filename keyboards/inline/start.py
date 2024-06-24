from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_kb():
  kb_list = [
		[InlineKeyboardButton(text="Упражнения", callback_data="training")],
		[InlineKeyboardButton(text="Программы тренировок", callback_data="program")],
		[InlineKeyboardButton(text="Питание", callback_data="menus")],
		[InlineKeyboardButton(text="Записаться на тренировку", callback_data="subscribe")]
	]
  
  return InlineKeyboardMarkup(inline_keyboard=kb_list)