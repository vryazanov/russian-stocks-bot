"""Menu handler."""
import telebot
import telebot.types

from bot import keyboards
from bot.actions.abc import BaseHandler


class Menu(BaseHandler):
    """Action to show menu."""

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Always return true."""
        return True

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Send menu keyboard"""
        text = 'Вы в меню. Выберете дальнейшее действие.'
        bot.send_message(message.chat.id, text, reply_markup=keyboards.menu)
