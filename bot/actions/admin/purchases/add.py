"""Add a new purchase."""
import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler


class Add(BaseHandler):
    """Handler to add a new purchase.."""

    @injector.inject
    def __init__(self):
        """Primary constructor."""

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's uknown user."""
        return message.text and message.text.startswith('/purchase-add')

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Parse / validate and save purchase."""
        text = 'Тут что-то будет.'
        bot.send_message(message.chat.id, text)
