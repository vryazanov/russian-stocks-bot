"""Protofio results."""
import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.storage import PurchaseStorage


class Results(BaseHandler):
    """Manage portfolio results."""

    command = '/results'

    @injector.inject
    def __init__(self, purchases: PurchaseStorage):
        """Primary constructor."""
        self._purchases = purchases

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's uknown user."""
        print(message)
        return message.text and message.text.startswith(self.command)

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Parse / validate and save purchase."""
        text = 'Тут что-то будет.'
        bot.send_message(message.chat.id, text)
