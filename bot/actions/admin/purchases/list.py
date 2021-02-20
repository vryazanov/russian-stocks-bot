"""List of purchases."""
import injector
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.storage import PurchaseStorage


class List(BaseHandler):
    """Show list of purchases."""

    command = '/purchases'

    @injector.inject
    def __init__(self, purchases: PurchaseStorage):
        """Primary constructor."""
        self._purchases = purchases

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if message contains purchase related json file."""
        return message.text == self.command

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Parse / validate and save purchase."""
        chunks = ['Список совершенных покупок:']
        for index, purchase in enumerate(self._purchases.all(), start=1):
            date_str = purchase.date.strftime('%Y-%m-%d')
            chunks.append(
                f'{index}. {date_str} на сумму '
                f'{purchase.cost} рублей.')

        bot.send_message(message.chat.id, '\n'.join(chunks))
