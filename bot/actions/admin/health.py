"""Menu handler."""
import telebot
import telebot.types

from bot.actions.abc import BaseHandler


class Health(BaseHandler):
    """Action to check health."""

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true."""
        return message.text == '/health'

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Send menu keyboard."""
        bot.send_message(message.chat.id, 'Все работает.')
