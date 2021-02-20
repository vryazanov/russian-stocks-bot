"""Add a new purchase."""
import injector
import pydantic
import telebot
import telebot.types

from bot.actions.abc import BaseHandler
from bot.entities import Purchase
from bot.storage import PurchaseStorage


class Add(BaseHandler):
    """Handler to add a new purchase."""

    @injector.inject
    def __init__(self, purchases: PurchaseStorage):
        """Primary constructor."""
        self._purchases = purchases

    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if message contains purchase related json file."""
        return (
            message.content_type == 'document'
            and message.document.mime_type == 'application/json')

    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Parse / validate and save purchase."""
        document = bot.get_file(message.document.file_id)
        content = bot.download_file(document.file_path)

        try:
            purchase = Purchase.parse_raw(content)
        except pydantic.ValidationError as e:
            text = f'Не могу сохранить покупку. Ошибка валидации:\n{e}'
            bot.send_message(message.chat.id, text)
        else:
            self._purchases.persist(purchase)
            bot.send_message(message.chat.id, 'Данные сохранены.')
