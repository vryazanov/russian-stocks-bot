"""Protofio results."""
import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.services import Portfolio


class Results(BaseHandler):
    """Manage portfolio results."""

    command = '/results'

    @injector.inject
    def __init__(self, portfolio: Portfolio):
        """Primary constructor."""
        self._portfolio = portfolio

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's a command to show results."""
        return message.text == self.command

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Prepare graph and send to the channel."""
        prices = self._portfolio.prices()
        text = '\n'.join(f'{date} - {price} рублей.' for date, price in prices)
        bot.send_message(message.chat.id, text)
