"""Ask user for vote."""
import injector
import telebot
import telebot.types

from bot import keyboards
from bot.actions.abc import BaseHandler
from bot.services import UserService
from bot.storage import UserStorage


class AskForVote(BaseHandler):
    """Action to ask user to vote for stocks."""

    command = '/askforvote'

    @injector.inject
    def __init__(self, storage: UserStorage, service: UserService):
        """Primary constructor."""
        self._storage = storage
        self._service = service

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if it's a command for this action."""
        return message.text == self.command

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Send a remined to user which still are not voted."""

        def is_user_to_notify(user) -> bool:
            if user.voting_state == 'finished':
                return False

            user.voting_state = None
            user.voting_steaks = 0
            user.voting_stocks = []
            self._storage.persist(user)
            return True

        num_of_notified = self._service.send_to_users(
            filter(is_user_to_notify, self._storage.all()),
            'Не забудьте проголосовать, голосование скоро завершится.',
            keyboards.menu)

        text = 'Кол-во оповещенных пользователей: {0}'.format(num_of_notified)
        bot.send_message(message.chat.id, text)
