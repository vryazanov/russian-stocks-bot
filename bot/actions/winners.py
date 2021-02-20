"""Show voting winners."""
import collections

import injector
import telebot.types

from bot.actions.abc import BaseHandler
from bot.actions.voting.constants import StateEnum
from bot.storage import UserStorage


class Winners(BaseHandler):
    """Command to show list of bot subcribers."""

    @injector.inject
    def __init__(self, storage: UserStorage):
        """Primary constructor."""
        self._storage = storage

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true for /users command."""
        return message.text == '/winners'

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Show winners of active voting."""
        users_voted = 0
        counter_stocks = collections.Counter()
        counter_steaks = collections.Counter()

        for user in self._storage.all():
            if user.voting_state == StateEnum.finished:
                users_voted += 1
                counter_stocks.update(user.voting_stocks)
                counter_steaks.update([user.voting_steaks])

        stocks = ', '.join(
            f'{ticker} [{votes}]'
            for ticker, votes in counter_stocks.most_common())
        steaks = ', '.join(
            f'{steak} [{votes}]'
            for steak, votes in counter_steaks.most_common())

        chunks = [
            f'Всего проголосовало: {users_voted}.',
            f'Голоса за тикеры: {stocks}.',
            f'Голоса за стейки: {steaks}.',
        ]

        bot.send_message(message.chat.id, '\n'.join(chunks))
