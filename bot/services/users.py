"""User related services."""
import logging
import typing

import telebot

from bot.entities import User
from bot.storage import UserStorage


LOGGER = logging.getLogger(__name__)


class UserService:
    """User service."""

    def __init__(self, bot: telebot.TeleBot, storage: UserStorage):
        """Primary constructor."""
        self._bot = bot
        self._storage = storage

    def send_to_user(
        self, user: User, text: str,
        keyboard: typing.Optional[telebot.types.JsonSerializable] = None,
    ) -> bool:
        """Send msg to user and handle if user blocked bot."""
        if user.is_blocked:
            return False

        try:
            self._bot.send_message(user.tg_id, text, reply_markup=keyboard)
        except Exception as e:
            LOGGER.info(f'Got error while sending text to user: {e}')
        else:
            return True

        user.is_blocked = True
        self._storage.persist(user)
        return False

    def send_to_users(
        self, users: typing.Iterable[User], text: str,
        keyboard: typing.Optional[telebot.types.JsonSerializable] = None,
    ) -> int:
        """Send message to a group of users."""
        def send_to_user(user: User):
            return self.send_to_user(user, text, keyboard)

        return sum(map(send_to_user, users))

    def send_to_all(
        self, text: str,
        keyboard: typing.Optional[telebot.types.JsonSerializable] = None,
    ) -> int:
        """Send message to all users."""
        return self.send_to_users(self._storage.all(), text, keyboard)
