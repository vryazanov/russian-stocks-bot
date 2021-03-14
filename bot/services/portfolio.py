"""Portfolio related services."""
import collections
import datetime
import decimal
import typing

import injector

from bot.entities import Purchase
from bot.services.stocks import StockService
from bot.storage import PurchaseStorage


def daterange(start_date, end_date) -> typing.Iterable[datetime.date]:
    """Iterate between two dates."""
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(n)


class Portfolio:
    """Manage assets portfolio here."""

    @injector.inject
    def __init__(self, service: StockService, purchases: PurchaseStorage):
        """Primary constructor."""
        self._service = service
        self._purchases = purchases

    def prices(self) -> typing.Tuple[datetime.date, decimal.Decimal]:
        """Compure price per dates."""
        purchases = sorted(self._purchases.all(), key=lambda p: p.date)

        if not purchases:
            return []

        today = datetime.datetime.today()
        start_date, end_date = purchases[0].date, today.date()

        last_prices, current_stocks = {}, collections.Counter()

        purchase_per_date: typing.Dict[datetime.date, Purchase]
        purchase_per_date = {purchase.date: purchase for purchase in purchases}

        results: typing.Tuple[datetime.date, decimal.Decimal] = []

        cash_left = 0

        for date in daterange(start_date, end_date):
            purchase = purchase_per_date.get(date)

            total_price = decimal.Decimal('0')

            for code, quantity in current_stocks.items():
                try:
                    price = self._service.quote(code, date).open_price
                except Exception:
                    price = last_prices.get(code, 0)
                else:
                    last_prices[code] = price

                total_price += price * quantity

            if purchase is not None:
                current_stocks.update({
                    stock.name: stock.quantity
                    for stock in purchase.stocks})
                total_price = purchase.cost
                cash_left += purchase.cash

            results.append((date, total_price + cash_left))

        return results
