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


admin_router = Router()


def get_column_names(cls):
    inspector = inspect(cls)
    return [column.name for column in inspector.columns]


@admin_router.message(Command("add_muscle"))
async def cmd_add_muscle(message: Message):
    if str(message.from_user.id) in ADMINS:
        args = message.text.split()[1:]

        muscle, muscle_type, video_id, status = args

        await DatabaseManager(model=Training, session_maker=SessionLocal).add(
            muscle=muscle, muscle_type=muscle_type, video_id=video_id, status=status
        )

        await message.reply("Упражнение добавлено")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("edit_muscle"))
async def cmd_edit_muscle(message: Message):
    if str(message.from_user.id) in ADMINS:
        args = message.text.split()[1:]

        id_, muscle, muscle_type, video_id, status = args

        await DatabaseManager(model=Training, session_maker=SessionLocal).update(
            int(id_), muscle=muscle, muscle_type=muscle_type, video_id=video_id, status=status
        )

        await message.reply("Упражнение изменено")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("delete_muscle"))
async def delete_muscle(message: Message):
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
async def get_table(message: Message):
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
async def get_video_id(message: Message):
    if str(message.from_user.id) in ADMINS:
        video_id = message.video.file_id
        await message.reply(f"ID видео: {video_id}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(F.content_type == ContentType.DOCUMENT)
async def get_document_id(message: Message):
    if str(message.from_user.id) in ADMINS:
        document_id = message.document.file_id
        await message.reply(f"ID документа: {document_id}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("send_document"))
async def send_document(message: Message):
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
async def get_document(message: Message):
    if str(message.from_user.id) in ADMINS:
        document_id = message.text.split()[1]

        await message.answer_document(document_id)
    else:
        await message.reply("У вас нет прав для выполнения этой команды")


@admin_router.message(Command("get_username"))
async def get_username(message: Message):
    if str(message.from_user.id) in ADMINS:
        user_id = message.text.split()[1]

        user = await bot.get_chat(int(user_id))
        username = user.username

        await message.answer(f"@{username}")
    else:
        await message.reply("У вас нет прав для выполнения этой команды")
        
        
@admin_router.message(Command("commands"))
async def get_commands(message: Message):
    await message.answer(
"""/add_muscle [muscle] [muscle_type] [video_id] - добавляет в базу данных упражнение. muscle - группа мышц (Спина), muscle_type - отдельная мыщца (Широчайшая), video_id - id видео\n
/edit_muscle [id] [muscle] [muscle_type] [video_id] - изменяет упражнение в базе данных. id - номер упражнения в базе данных, muscle, muscle_type, video_id - новые значения\n
/delete_muscle [id] - удаляет упражнение из базы данных. id - номер упражнения в базе данных\n
/get_table [table_name] - показывает структуру таблицы. Таблицы в боте: trainings, menus, programs, questionnaire. trainings - упражнения, menus - меню, programs - программы, questionnaire - анкеты пользователей, а также тип анкеты (Программа тренировок, Меню)\n
/send_document [user_id] [document_type] [document_id] - отправляет документ пользователю. user_id - id пользователя, document_type - тип документа (Меню/Программа), document_id - id документа\n
/get_document [document_id] - показывает документ. document_id - id документа\n
/get_username [user_id] - показывает имя пользователя. user_id - id пользователя\n
Отправка видео или документа - администратор получит ID файла, который можно использовать в будущем. Пример использования:\n
Пользователь попросил составить ему программу тренировок. Информация занесена в базу данных. Там хранится его ID. Тренер составил программу. Администратор отправляет в чат с ботом файл, бот возвращает ему ID документа, после чего можно отправить его в чат с пользователем.
"""
    )
