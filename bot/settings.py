"""Keep bot settings here."""
import os
import pathlib


BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_ADMIN_GROUP = int(os.environ['BOT_ADMIN_GROUP'])

STORAGE_PATH = pathlib.Path(os.environ['STORAGE_PATH'])
