"""Welcome handler."""
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.services import VotingManager, UserService


class StartVoting(BaseHandler):
    """Initial handler."""

    def __init__(self, users: UserService, manager: VotingManager):
        """Primary constructor."""
        self._users = users
        self._manager = manager

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's uknown user."""
        return message.text and message.text.startswith('/startvoting')

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Parse and validate payload, start voting if everything is ok."""
        if self._manager.current():
            text = 'Остановите текущее голосование прежде чем начать новое.'
            bot.send_message(message.chat.id, text)
            return

        raw_payload = message.text.replace('/startvoting', '').strip()
        payload_chunks = raw_payload.split()

        max_stocks, max_steaks = None, None

        for chunk in filter(lambda chunk: '=' in chunk, payload_chunks):
            name, value = chunk.rsplit('=')

            if value.isdigit():
                if name == 'stocks':
                    max_stocks = int(value)
                elif name == 'steaks':
                    max_steaks = int(value)

        if max_steaks is None or max_stocks is None:
            text = 'Не могу распарсить параметы голосования.'
            bot.send_message(message.chat.id, text)
            return

        self._manager.start(max_stocks, max_steaks)

        text = 'Управляющий портфелем запустил новое голосование.'
        num = self._users.send_to_all(text)

        text = f'Голосования запущено. Оповещено пользователей: {num}'
        bot.send_message(message.chat.id, text)
