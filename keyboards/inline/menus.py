from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_promgrams_kb():
  kb_list = [
    [InlineKeyboardButton(text="Готовые меню", callback_data="ready_programs")],
    [InlineKeyboardButton(text="Персональное меню", callback_data="personal_program")],
		[InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
	]
  
  return InlineKeyboardMarkup(inline_keyboard=kb_list)


def get_ready_programs_kb():
	kb_list = [
		[InlineKeyboardButton(text="Похудение", callback_data="weight_loss")],
		[InlineKeyboardButton(text="Набор мышечной массы", callback_data="muscle_gain")],
		[InlineKeyboardButton(text="Поддержание формы", callback_data="form_support")],
		[InlineKeyboardButton(text="Назад", callback_data="back_to_programs")]
	]
 
	return InlineKeyboardMarkup(inline_keyboard=kb_list)
  