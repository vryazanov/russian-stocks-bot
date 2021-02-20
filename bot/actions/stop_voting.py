"""Welcome handler."""
import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.services import VotingManager, UserService
from bot.storage import UserStorage, VotingStorage


class StopVoting(BaseHandler):
    """Stop active voting."""

    @injector.inject
    def __init__(self, manager: VotingManager):
        """Primary constructor."""
        self._manager = manager

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's uknown user."""
        return message.text and message.text.startswith('/stopvoting')

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Parse and validate payload, start voting if everything is ok."""
        finished = self._manager.stop()

        if finished:
            text = 'Голосование завершено.'
        else:
            text = 'Голосование не запущено.'

        bot.send_message(message.chat.id, text)
