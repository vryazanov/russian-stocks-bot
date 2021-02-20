"""Voting responses."""
import typing

import telebot
import telebot.types

from bot.constants import Commands


def keyboard_steaks(max_steaks: int):
    """Keyboard for steak voting."""
    buttons = [
        telebot.types.KeyboardButton(steak)
        for steak in range(1, max_steaks + 1)]

    keyboard = telebot.types.ReplyKeyboardMarkup(
        row_width=3, resize_keyboard=True)
    keyboard.add(*buttons)

    return keyboard


def keyboard_stocks(stocks: typing.List[str], commands: typing.List[Commands]):
    """Keyboard for stocks voting."""
    keyboard = telebot.types.ReplyKeyboardMarkup(
        row_width=3, resize_keyboard=True)
    keyboard.row(*[telebot.types.KeyboardButton(cmd) for cmd in commands])
    keyboard.add(*[telebot.types.KeyboardButton(stock) for stock in stocks])
    return keyboard


def keyboard_menu():
    """Keyboatd - back to menu."""
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        telebot.types.KeyboardButton(Commands.repeat_voting),
        telebot.types.KeyboardButton(Commands.to_menu),
    )
    return keyboard


class Reply:
    """Helper to reply messages."""

    def __init__(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Primary constructor."""
        self._bot = bot
        self._message = message

    def send(
        self, text: str,
        keyboard: typing.Optional[telebot.types.JsonSerializable] = None,
    ):
        """Reply to message."""
        self._bot.reply_to(self._message, text, reply_markup=keyboard)
