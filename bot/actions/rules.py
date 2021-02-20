"""Rules handler."""
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.constants import Commands


class Rules(BaseHandler):
    """Action that shows rules."""

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if user wants rules."""
        return message.text == Commands.rules

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Save user to storage and send welcome message."""
        text = open('./articles/rules.txt').read()

        keyboard = telebot.types.ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
        )
        keyboard.add(
            telebot.types.KeyboardButton(Commands.start_voting),
            telebot.types.KeyboardButton(Commands.rules),
        )

        bot.send_message(message.chat.id, text, reply_markup=keyboard)
