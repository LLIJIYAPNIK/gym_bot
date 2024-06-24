from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.filters import Command
from database.models import Training
from database.session import SessionLocal
from database.crud import DatabaseManager
from database.models import Base
from xlsxwriter import Workbook
import os
from sqlalchemy import inspect
from config import ADMINS, TABLES
from create_bot import bot
from aiogram.fsm.context import FSMContext


admin_router = Router()


def get_column_names(cls):
    inspector = inspect(cls)
    return [column.name for column in inspector.columns]


@admin_router.message(Command("add_muscle"))
async def cmd_add_muscle(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        args = message.text.split()[1:]

        muscle, muscle_type, video_id = args

        await DatabaseManager(model=Training, session_maker=SessionLocal).add(
            muscle=muscle, muscle_type=muscle_type, video_id=video_id
        )

        await message.reply("Упражнение добавлено")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("edit_muscle"))
async def cmd_edit_muscle(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        args = message.text.split()[1:]

        id_, muscle, muscle_type, video_id = args

        await DatabaseManager(model=Training, session_maker=SessionLocal).update(
            int(id_), muscle=muscle, muscle_type=muscle_type, video_id=video_id
        )

        await message.reply("Упражнение изменено")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("delete_muscle"))
async def delete_muscle(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        args = message.text.split()[1:]

        id_ = args

        await DatabaseManager(model=Training, session_maker=SessionLocal).delete(
            int(id_)
        )

        await message.reply("Упражнение удалено")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("get_table"))
async def get_table(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        table_name = message.text.split()[1]
        if table_name in TABLES:
            model = Base.metadata.tables[
                table_name
            ]  # Предполагается, что table_name соответствует имени таблицы в базе данных

            db_manager = DatabaseManager(model=model, session_maker=SessionLocal)
            data = list(await db_manager.get_all(model))

            file_path = f"{table_name}.xlsx"
            workbook = Workbook(file_path)
            worksheet = workbook.add_worksheet()

            count = 0
            for elem in get_column_names(model):
                worksheet.write(0, count, str(elem))
                count += 1

            for row, row_data in enumerate(data):
                for col, value in enumerate(row_data):
                    worksheet.write(row + 1, col, str(value))
            workbook.close()

            input_file = FSInputFile(path=file_path)
            await message.answer_document(
                input_file, caption=f"Структура таблицы   {table_name}"
            )

            os.remove(file_path)
        else:
            await message.reply("Такая таблица не существует")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(F.content_type == ContentType.VIDEO)
async def get_video_id(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        video_id = message.video[-1].file_id
        await message.reply(f"ID видео: {video_id}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(F.content_type == ContentType.DOCUMENT)
async def get_document_id(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        document_id = message.document.file_id
        await message.reply(f"ID документа: {document_id}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("send_document"))
async def send_document(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        args = message.text.split()[1:]

        user_id, document_type, document_id = args
        if document_type.lower() in ["меню", "программа"]:
            try:
                await bot.forward_messages(
                    chat_id=user_id,
                    from_chat_id=message.chat.id,
                    message_id=document_id,
                )
            except ValueError:
                await message.reply(
                    "Неверный ID документа/пользователя. Использование: /send_document [user_id] [document_type] [document_id]"
                )
        else:
            await message.reply("Такого типа документа нет. (Меню/Программа)")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("get_document"))
async def get_document(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        document_id = message.text.split()[1]

        await message.answer_document(document_id)
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("get_username"))
async def get_username(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        user_id = message.text.split()[1]

        user = await bot.get_chat(int(user_id))
        username = user.username

        await message.answer(f"@{username}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")
