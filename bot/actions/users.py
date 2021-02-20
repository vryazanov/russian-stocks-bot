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
        text = 'Подписчиков у бота: {0}'.format(len(self._storage.all()))
        bot.send_message(message.chat.id, text)
