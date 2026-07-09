import os
from pathlib import Path
from dotenv import load_dotenv

DIR = Path(__file__).absolute().parent
ENV_PATH = DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")