import os
import pathlib


BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_ADMIN_GROUP = int(os.environ['BOT_ADMIN_GROUP'])

STORAGE_PATH = pathlib.Path(os.environ['STORAGE_PATH'])

STOCKS_BASE_URL = os.environ['STOCKS_BASE_URL']
