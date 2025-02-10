import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TESSERACT_PATH = os.getenv('TESSERACT_PATH')
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')