"""Action groups."""
import telebot.types

from bot.actions.abc import BaseGroup


class PrivateMessage(BaseGroup):
    """Allow only private messages."""

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if message type in private."""
        return message.chat.type == 'private'


class Group(BaseGroup):
    """Allow only in admin group."""

    def __init__(self, chat_id: int, *args, **kwargs):
        """Primary constructor."""
        super().__init__(*args, **kwargs)
        self._chat_id = chat_id

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if message type in private."""
        return message.chat.id == self._chat_id
