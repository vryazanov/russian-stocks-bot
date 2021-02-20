"""Classes to wotk with stocks."""
import datetime
import typing
import urllib.parse

import requests

import bot.entities


class StockError(Exception):
    """Base exception for any errors from stock service."""


class NoPriceFound(StockError):
    """Raise if price not found."""


class StockService:
    """Service to fetch stocks in a provided order."""

    def __init__(self, url: str, ordered: typing.List[str]):
        """Primary instructor."""
        self._url = url
        self._ordered = ordered

    def fetch(self) -> typing.List[bot.entities.Stock]:
        """Return list of entities."""
        stocks = []
        response = requests.get(urllib.parse.urljoin(self._url, '/tickers'))

        for stock_data in response.json()['results']:
            if stock_data['lot'] and stock_data['code'] in self._ordered:
                stocks.append(
                    bot.entities.Stock(
                        name=stock_data['name'],
                        code=stock_data['code'],
                        lot=stock_data['lot'],
                        order=self._ordered.index(stock_data['code']),
                    ),
                )

        return sorted(stocks, key=lambda stock: stock.order)

    def quote(self, code: str, date: datetime.date) -> bot.entities.Quote:
        """Return price of specific stock code for specific date."""
        path = '/tickers/{0}/quotes/{1}'.format(
            code, date.strftime('%Y-%m-%d'))
        url = urllib.parse.urljoin(self._url, path)

        response = requests.get(url)
        prices = response.json()['results']

        if not prices:
            raise NoPriceFound

        return bot.entities.Quote(**prices[0])
