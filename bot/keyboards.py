"""Common keayboards."""
import telebot.types

from bot.constants import Commands


menu = telebot.types.ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
)
menu.add(
    telebot.types.KeyboardButton(Commands.start_voting),
    telebot.types.KeyboardButton(Commands.rules),
)
