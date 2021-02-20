"""User related services."""
import logging

import telebot

from bot.storage import UserStorage


LOGGER = logging.getLogger(__name__)


class UserService:
    """User service."""

    def __init__(self, bot: telebot.TeleBot, storage: UserStorage):
        """Primary constructor."""
        self._bot = bot
        self._storage = storage

    def send_to_all(self, text: str) -> int:
        """Send message to all users."""
        cnt = 0
        for user in self._storage.all():
            try:
                self._bot.send_message(user.tg_id, text)
            except Exception as e:
                LOGGER.info(f'Got error while sending text to user: {e}')
            else:
                cnt += 1
        return cnt
