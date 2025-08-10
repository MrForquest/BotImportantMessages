import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent  # .parent

# Load environment variables
load_dotenv()
env = dotenv_values()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REPORT_CHANNEL_ID = os.getenv("REPORT_CHANNEL_ID")
IN_TEXT = os.getenv("IN_TEXT").split(", ")
CHAT_ID = int(os.getenv("SHIK_ID"))
TEST_ID = int(os.getenv("TEST_ID"))
BOT_ADMIN_ID = int(os.getenv("BOT_ADMIN_ID"))

GPT_TOKEN = os.getenv("GPT_TOKEN")

DATABASE_PATH = BASE_DIR / "db" / "curse_words.db"
