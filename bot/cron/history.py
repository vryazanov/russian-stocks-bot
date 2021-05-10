import csv
import io
import logging
import typing

import requests

from bot.entities import QuoteItem, Quotes
from bot.storage import PurchaseStorage, QuotesStorage


LOGGER = logging.getLogger(__name__)

# TO BE UPDATED

params = {
    'from': '2021-02-01',
    'to': '2021-05-09',
    'api_token': '6071b1161ae602.16550571',
    'prediod': 'd',
}


def iter_over_csv(text: str) -> typing.Iterable[
    typing.Tuple[str, float, float],
]:
    """Extract date / open price / close price from csv based content."""
    reader = csv.reader(io.StringIO(text))

    for index, row in enumerate(reader):
        if index == 0:
            # skip headers
            continue

        try:
            date, open_price, _, _, close_price, *_ = row
        except ValueError:
            # last line contains only one column
            continue

        yield date, open_price, close_price


def fetch_one(exchange: str, ticker: str):
    """Fetch quotes for specific ticker."""
    url = 'https://eodhistoricaldata.com/api/eod/{ticker}.{exchange}'.format(
        ticker=ticker,
        exchange=exchange,
    )

    response = requests.get(url, params=params)

    quotes = []
    for date, open_price, close_price in iter_over_csv(response.text):
        quotes.append(QuoteItem(
            date=date,
            open_price=open_price,
            close_price=close_price,
        ))

    return Quotes(name=ticker, quotes=quotes)


def fetch(purchases: PurchaseStorage, historical: QuotesStorage):
    """Fetch historical quotes for all tickers."""
    tickers = set()

    for purchase in purchases.all():
        for stock in purchase.stocks:
            tickers.add(stock.name)

    for ticker in tickers:
        try:
            quotes = fetch_one('MCX', ticker)
        except Exception as e:
            LOGGER.exception(str(e))

        historical.persist(quotes)
