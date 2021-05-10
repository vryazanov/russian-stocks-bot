"""Classes to wotk with stocks."""
import datetime

import bot.entities
import bot.storage


class StockError(Exception):
    """Base exception for any errors from stock service."""


class NoPriceFound(StockError):
    """Raise if price not found."""


class StockService:
    """Service to fetch stocks in a provided order."""

    def __init__(self, historical: bot.storage.QuotesStorage):
        """Primary instructor."""
        self._historical = historical

    def quote(self, code: str, date: datetime.date) -> bot.entities.QuoteItem:
        """Return price of specific stock code for specific date."""
        quotes = self._historical.get(code)

        for item in quotes.quotes:
            if item.date == date:
                return item
        return None
