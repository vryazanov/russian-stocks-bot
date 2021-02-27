"""Action to dump storages."""
import datetime
import os
import pathlib
import tempfile
import zipfile

import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.settings import STORAGE_PATH


class Dump(BaseHandler):
    """Dump storages and send to admin group."""

    command = '/dump'

    def __init__(self, path: str = STORAGE_PATH):
        """Primary constructor."""
        self._path = pathlib.Path(path)

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's a command for this action."""
        return message.text == self.command

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Dump storages to archive and send to channel."""
        with tempfile.TemporaryDirectory() as folder:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            path_to_archive = os.path.join(folder, f'dump-{today}.zip')

            with zipfile.ZipFile(path_to_archive, 'w') as myzip:
                for file_ in self._path.glob('*.json'):
                    myzip.write(file_)

            archive = open(path_to_archive, 'rb')
            bot.send_document(message.chat.id, archive)
