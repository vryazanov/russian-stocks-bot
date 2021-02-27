"""Manage list of users."""
import injector
import telebot.types

from bot.actions.abc import BaseHandler
from bot.storage import UserStorage


class Users(BaseHandler):
    """Command to show list of bot subcribers."""

    @injector.inject
    def __init__(self, storage: UserStorage):
        """Primary constructor."""
        self._storage = storage

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true for /users command."""
        return message.text == '/users'

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Show list of bot's subscribers."""
        active, blocked = 0, 0

        for user in self._storage.all():
            if user.is_blocked:
                blocked += 1
            else:
                active += 1

        text = (
            'Активных подписчиков у бота: {0}.\n'
            'Заблокировали: {1}'
        ).format(active, blocked)

        bot.send_message(message.chat.id, text)
