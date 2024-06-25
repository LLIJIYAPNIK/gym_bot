from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.crud import DatabaseManager
from database.session import SessionLocal
from database.models import Training
import random
import json


class MuscleKeyboard:
    def __init__(self):
        self.translations = self.load_translations()

    def load_translations(self):
        try:
            with open("translations.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_translations(self):
        with open("translations.json", "w", encoding="utf-8") as f:
            json.dump(self.translations, f, ensure_ascii=False, indent=4)

    def get_or_create_translation(self, russian):
        if russian not in self.translations:
            self.translations[russian] = self.create_value()
            self.save_translations()
        return self.translations[russian]

    async def get_main_keyboard(self):
        kb_list = []
        muscles = set(
            await DatabaseManager(Training, SessionLocal).get_by_condition(
                condition=(Training.muscle != None),
                quantity=True,
                select_this=Training.muscle,
            )
        )

        for muscle in muscles:
            callback_data = self.get_or_create_translation(muscle)
            kb_list.append(
                [InlineKeyboardButton(text=muscle, callback_data=str(callback_data))]
            )

        kb_list.append(
            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
        )

        return InlineKeyboardMarkup(inline_keyboard=kb_list)

    async def get_sub_keyboard(self, muscle: str):
        kb_list = []
        trainings = set(
            await DatabaseManager(Training, SessionLocal).get_by_condition(
                condition=(Training.muscle == muscle),
                quantity=True,
                select_this=Training.muscle_type,
            )
        )

        for muscle_type in trainings:
            callback_data = self.get_or_create_translation(muscle_type)
            kb_list.append(
                [
                    InlineKeyboardButton(
                        text=" ".join(muscle_type.split("_")), callback_data=str(callback_data)
                    )
                ]
            )

        kb_list.append(
            [InlineKeyboardButton(text="Назад", callback_data="back_to_training")]
        )

        return InlineKeyboardMarkup(inline_keyboard=kb_list)

    def create_value(self):
        num = random.randint(0, 1000)
        while True:
            if num not in self.translations.values():
                return num
            else:
                num = random.randint(0, 1000)
