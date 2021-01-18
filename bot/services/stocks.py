"""Classes to wotk with stocks."""
import pathlib
import typing

import requests

import bot.entities


class StockService:
    """Service to fetch stocks in a provided order."""

    def __init__(self, url: str, ordered: typing.List[str]):
        """Primary instructor."""
        self._url = url
        self._ordered = ordered

    def fetch(self) -> typing.List[bot.entities.Stock]:
        """Return list of entities."""
        stocks = []
        response = requests.get(self._url)

        for stock_data in response.json()['results']:
            if stock_data['lot'] and stock_data['code'] in self._ordered:
                stocks.append(
                    bot.entities.Stock(
                        name=stock_data['name'],
                        code=stock_data['code'],
                        lot=stock_data['lot'],
                        order=self._ordered.index(stock_data['code'])
                    )
                )

        return list(sorted(stocks, key=lambda stock: stock.order))
