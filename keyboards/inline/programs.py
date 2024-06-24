from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_program_train_kb():
    kb_list = [
        [InlineKeyboardButton(text="Готовые программы", callback_data="ready_trains")],
        [
            InlineKeyboardButton(
                text="Персональная программа", callback_data="personal_trains"
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def get_ready_programs_trains_kb():
    kb_list = [
        [InlineKeyboardButton(text="Программа 1", callback_data="pr1")],
        [InlineKeyboardButton(text="Программа 2", callback_data="pr2")],
        [InlineKeyboardButton(text="Программа 3", callback_data="pr3")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_program")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb_list)
