"""StateEnum machine."""
import typing

import transitions

from bot.actions.voting import reply
from bot.actions.voting.constants import ActionEnum, StateEnum
from bot.constants import Commands
from bot.entities import User


Stocks = typing.List[str]


class Machine:

    def __init__(self, state: StateEnum, reply: reply.Reply):
        """Primary constructor."""
        self._reply = reply
        self._machine = transitions.Machine(
            model=self, states=StateEnum, initial=state, transitions=[
                {
                    'source': StateEnum.initial, 
                    'trigger': ActionEnum.ask_for_stocks,
                    'dest': StateEnum.waiting_for_stock,
                    'before': 'on_stock_initial',
                },
                # if nothing to buy button is clicked
                {
                    'source': StateEnum.waiting_for_stock,
                    'trigger': ActionEnum.vote_for_stock,
                    'dest': StateEnum.finished,
                    'conditions': ['is_nothing_to_buy_cmd'],
                    'before': ['on_finish_nothing_to_buy'],
                },
                # if nothing more button is clicked
                {
                    'source': StateEnum.waiting_for_stock,
                    'trigger': ActionEnum.vote_for_stock,
                    'dest': StateEnum.nothing_more,
                    'conditions': ['is_nothing_more_cmd'],
                },
                # if revote button is clicked
                {
                    'source': StateEnum.waiting_for_stock,
                    'trigger': ActionEnum.vote_for_stock,
                    'dest': StateEnum.revote,
                    'conditions': ['is_revote_cmd'],
                },
                # if stock is invalid
                {
                    'source': StateEnum.waiting_for_stock,
                    'trigger': ActionEnum.vote_for_stock,
                    'dest': StateEnum.waiting_for_stock,
                    'unless': ['is_stock_valid'],
                    'before': ['on_stock_invalid'],
                },
                # stock is good
                {
                    'source': StateEnum.waiting_for_stock,
                    'trigger': ActionEnum.vote_for_stock,
                    'dest': StateEnum.stock,
                },
                # need one more stock
                {
                    'source': StateEnum.stock,
                    'trigger': ActionEnum.ask_for_stocks,
                    'dest': StateEnum.waiting_for_stock,
                    'before': ['on_stock_more'],
                },                
                # start voting for steaks
                {
                    'source': StateEnum.stock,
                    'trigger': ActionEnum.ask_for_steaks,
                    'dest': StateEnum.waiting_for_steak,
                    'before': ['on_steak_initial'],
                },
                # if voting for steaks is not needed
                {
                    'source': StateEnum.stock,
                    'trigger': ActionEnum.finish,
                    'dest': StateEnum.finished,
                    'before': ['on_finish_no_steaks'],
                },
                # specific commands
                {
                    'source': StateEnum.nothing_more,
                    'trigger': ActionEnum.ask_for_steaks,
                    'dest': StateEnum.waiting_for_steak,
                    'before': ['on_steak_initial'],
                },
                {
                    'source': StateEnum.nothing_more,
                    'trigger': ActionEnum.finish,
                    'dest': StateEnum.finished,
                    'before': ['on_finish_no_steaks'],
                },
                {
                    'source': StateEnum.revote,
                    'trigger': ActionEnum.ask_for_stocks,
                    'dest': StateEnum.waiting_for_stock,
                    'before': 'on_stock_initial',
                },
                # if voted steak is invalid
                {
                    'source': StateEnum.waiting_for_steak,
                    'trigger': ActionEnum.vote_for_steak,
                    'dest': StateEnum.waiting_for_steak,
                    'unless': ['is_steak_valid'],
                    'before': ['on_steak_invalid']
                },
                # steak is good
                {
                    'source': StateEnum.waiting_for_steak,
                    'trigger': ActionEnum.vote_for_steak,
                    'dest': StateEnum.steak,
                },
                # finish voting flow
                {
                    'source': StateEnum.steak,
                    'trigger': ActionEnum.finish,
                    'dest': StateEnum.finished,
                    'before': ['on_finish'],
                },     
                # repeat
                {
                    'source': StateEnum.finished,
                    'trigger': ActionEnum.repeat,
                    'dest': StateEnum.initial,
                },
            ])

    def on_stock_initial(self, stocks: Stocks, max_stocks: int):
        """User is ready to vote for stocks."""
        text = 'Что будем покупать? Максимум компаний для покупки ' \
               'в этот раз: {}.'.format(max_stocks)
        keyboard = reply.keyboard_stocks(stocks, [Commands.nothing_to_buy])
        self._reply.send(text, keyboard)

    def on_stock_invalid(self, stocks: Stocks, stock: str):
        """User voted for invalid stock."""
        text = 'Не могу найти такой тикер. Выберете один из предложенных.'
        self._reply.send(text)

    def on_stock_more(self, stocks: Stocks):
        """Need more stocks."""
        text = 'Отлично, давай выберем что-нибудь еще.'
        keyboard = reply.keyboard_stocks(
            stocks, [Commands.nothing_more, Commands.repeat_voting])
        self._reply.send(text, keyboard)

    def on_steak_initial(self, max_steaks: int):
        """User is ready to vote for steaks."""
        text = 'Отлично, теперь надо определиться сколько стейков ' \
               'мы будем инвестировать. Выберете один из вариантов.'
        keyboard = reply.keyboard_steaks(max_steaks)
        self._reply.send(text, keyboard)

    def on_steak_invalid(self, max_steaks: int, steaks: str):
        text = 'Выберете один из предложенных вариантов.'
        self._reply.send(text)

    def on_finish(self, stocks: Stocks, steaks: int):
        """When user finish voting."""
        text = 'Ставки сделаны, ставок больше нет! Вы проголосовали за: ' \
               '{stocks}. И желаете инвестировать стейков: {steaks}.'.format(
                   stocks=', '.join(stocks),
                   steaks=steaks,
               )
        self._reply.send(text, reply.keyboard_menu())

    def on_finish_nothing_to_buy(self, stocks: Stocks, command: str):
        """User wants not to buy this time."""
        text = 'Ваш голос принят. Вы проголосовали против покупок в этот раз.'
        self._reply.send(text, reply.keyboard_menu())

    def on_finish_no_steaks(self, stocks: Stocks):
        text = 'Голос принят, ваш выбор: {stocks}. В этот раз за кол-во ' \
               'стейков не голосуем, т.к. доступен только один ' \
               'стейк к покупке.'.format(stocks=', '.join(stocks))
        self._reply.send(text, reply.keyboard_menu())

    def is_nothing_to_buy_cmd(self, stocks: Stocks, command: str) -> bool:
        """Return true for `nothing to buy command`."""
        return command == Commands.nothing_to_buy

    def is_nothing_more_cmd(self, stocks: Stocks, command: str) -> bool:
        """Return true for `nothing more` command."""
        return command == Commands.nothing_more

    def is_revote_cmd(self, stocks: Stocks, command: str) -> bool:
        """Return true for revote command."""
        return command == Commands.repeat_voting

    def is_stock_valid(self, stocks: Stocks, stock: str):
        """Return true if stock is valid."""
        return stock in stocks

    def is_steak_valid(self, max_steaks: int, steaks: str):
        """Check if user sent correct value."""
        return steaks in [str(steak) for steak in range(1, max_steaks + 1)]
