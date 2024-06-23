from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
ADMINS = os.getenv('ADMINS').split(',')
TABLES=['users', 'trainings', 'programs', 'menus']
VIDEO_DIR = os.getenv('VIDEO_DIR')