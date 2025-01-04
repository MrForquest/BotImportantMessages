from pathlib import Path

from dotenv import dotenv_values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent  # .parent

# Load environment variables
ENV_NAME = ".env"
ENV_PATH = BASE_DIR / ENV_NAME
env = dotenv_values(ENV_PATH)

BOT_TOKEN = env.get("BOT_TOKEN")
REPORT_CHANNEL_ID = env.get("REPORT_CHANNEL_ID")
IN_TEXT = env.get("IN_TEXT").split(", ")

CHATGPT_KEY = env.get("CHATGPT_KEY")

DATABASE_PATH = BASE_DIR / "db" / "curse_words.db"
