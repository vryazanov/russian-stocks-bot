"""Welcome handler."""
import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.constants import Commands
from bot.entities import User
from bot.storage import NoEntityFound, UserStorage


class Welcome(BaseHandler):
    """Initial handler."""

    @injector.inject
    def __init__(self, storage: UserStorage):
        """Primary constructor."""
        self._storage = storage

    def is_new_user(self, user_id: int) -> bool:
        """Check if user is new."""
        try:
            self._storage.get(str(user_id))
        except NoEntityFound:
            return True
        return False

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's uknown user."""
        return self.is_new_user(message.from_user.id)

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Save user to storage and send welcome message."""
        if self.is_new_user(message.from_user.id):
            self._storage.persist(
                User(
                    tg_id=message.from_user.id,
                    tg_username=message.from_user.username,
                    tg_first_name=message.from_user.first_name,
                    tg_last_name=message.from_user.last_name,
                ),
            )

        text = open('./articles/welcome.txt').read()

        keyboard = telebot.types.ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True,
        )
        keyboard.add(
            telebot.types.KeyboardButton(Commands.start_voting),
            telebot.types.KeyboardButton(Commands.rules),
        )

        bot.send_message(message.chat.id, text, reply_markup=keyboard)
