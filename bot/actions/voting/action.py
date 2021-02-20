"""Voting handler."""
import typing

import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.actions.voting.constants import StateEnum
from bot.actions.voting.machine import Machine
from bot.actions.voting.reply import Reply
from bot.constants import Commands
from bot.entities import Stock
from bot.keyboards import menu
from bot.services import VotingManager
from bot.storage import UserStorage


class Voting(BaseHandler):
    """Manage voting flow."""

    @injector.inject
    def __init__(
        self, manager: VotingManager, storage: UserStorage,
        stocks: typing.List[Stock],
    ):
        """Primary constructor."""
        self._manager = manager
        self._storage = storage
        self._stocks = stocks

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if voting mode is enabled."""
        if message.text in (Commands.start_voting, Commands.repeat_voting):
            return True

        user = self._storage.get(message.from_user.id)

        if user.voting_state is None:
            return False

        return user.voting_state != StateEnum.finished

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Handle user action based on current state."""
        user = self._storage.get(message.from_user.id)

        reply = Reply(bot, message)
        machine = Machine(user.voting_state or StateEnum.initial, reply)

        voting = self._manager.current()

        if not voting:
            reply.send('В данный момент голосование недоступно.', menu)
            user.voting_state = None
            self._storage.persist(user)
            return

        if machine.is_finished():
            user.voting_stocks = []
            user.voting_steaks = 0
            machine.repeat()

        max_stocks = voting.max_stocks
        max_steaks = voting.max_steaks

        def get_stocks() -> typing.List[Stock]:
            return [
                stock.name for stock in self._stocks
                if stock.name not in user.voting_stocks]

        if machine.is_initial():
            machine.ask_for_stocks(get_stocks(), max_stocks)
        elif machine.is_waiting_for_stock():
            machine.vote_for_stock(get_stocks(), message.text)

            if machine.is_stock():
                user.voting_stocks.append(message.text)

                if len(user.voting_stocks) == max_stocks:
                    if max_steaks == 1:
                        user.voting_steaks = 1
                        machine.finish(user.voting_stocks)
                    else:
                        machine.ask_for_steaks(max_steaks)
                else:
                    machine.ask_for_stocks(get_stocks())
            elif machine.is_revote():
                user.voting_stocks = []
                user.voting_steaks = 0
                machine.ask_for_stocks(get_stocks(), max_stocks)
            elif machine.is_nothing_more():
                if max_steaks == 1:
                    user.voting_steaks = 1
                    machine.finish(user.voting_stocks)
                else:
                    machine.ask_for_steaks(max_steaks)

        elif machine.is_waiting_for_steak():
            machine.vote_for_steak(max_steaks, message.text)

            if machine.is_steak():
                user.voting_steaks = int(message.text)
                machine.finish(user.voting_stocks, user.voting_steaks)

        user.voting_state = machine.state
        self._storage.persist(user)
