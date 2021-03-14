"""Protofio results."""
import injector
import matplotlib.pyplot as plt
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.services import Portfolio


class Results(BaseHandler):
    """Manage portfolio results."""

    step = 500
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
        min_value, max_value, x, y = None, None, [], []

        for date, price in self._portfolio.prices():
            x.append(date.strftime('%y.%m.%d'))
            y.append(price)

            if max_value is None or price > max_value:
                max_value = price
            if min_value is None or price < min_value:
                min_value = price

        fig, ax = plt.subplots()

        ax.plot(x, y, label='Народный портфель')
        ax.xaxis.set_major_locator(plt.AutoLocator())

        min_y = int(min_value // self.step)
        max_y = int(max_value // self.step) + 2

        ticks = [tick * self.step for tick in range(min_y, max_y + 1)]

        plt.yticks(ticks)
        plt.legend()
        plt.savefig('lines.png', format='png')

        bot.send_photo(message.chat.id, open('lines.png', 'rb'))

        # ------------

        labels = ('Кэш', 'Лукойл', 'Сбербанк-п', 'НорНикель')
        fracs = [15, 30, 45, 10]

        fig, (ax1, ax2) = plt.subplots(1, 2)

        ax1.pie(fracs, labels=labels, radius=1, explode=(0.1, 0, 0, 0))
        ax1.set_title('Народный портфель')

        ax2.pie(fracs, labels=labels, radius=1, explode=(0.1, 0, 0, 0))
        ax2.set_title('HeySteak портфель')

        plt.savefig('pie.png', format='png')
        bot.send_photo(message.chat.id, open('pie.png', 'rb'))
