"""Portfolio related services."""
import collections
import datetime
import decimal
import typing

import injector

from bot.services.deal import Deal
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
        """Compute price per dates."""
        purchases = {
            purchase.date: purchase
            for purchase in self._purchases.all()}

        if not purchases:
            return

        start_date = datetime.date(2021, 2, 1)
        end_date = datetime.date(2021, 4, 1)

        current_portfolio: collections.Counter[str, int] = {}

        for date in daterange(start_date, end_date):

            if date in purchases:
                current_portfolio.update({
                    stock.name: stock.quantity
                    for stock in purchases[date].stocks})
            price = self._price_for_stocks(date, current_portfolio)

            if price is not None:
                yield date, price

    def assets(self, date: datetime.date) -> typing.Dict[str, decimal.Decimal]:
        """Return stocks and their prices."""
        stocks = collections.Counter()

        for purchase in self._purchases.all():
            stocks.update({
                stock.name: stock.quantity
                for stock in purchase.stocks})

        return {
            stock: self._service.quote(stock, date).close_price * quantity
            for stock, quantity in stocks.items()}

    def _price_for_stocks(
        self, date: datetime.date, stocks: typing.Dict[str, int],
    ) -> decimal.Decimal:
        result = decimal.Decimal('0.0')

        for name, quantity in stocks.items():
            quote = self._service.quote(name, date)

            if quote is None:
                return None

            result += quote.close_price * quantity

        return result


class Portfolio:

    def __init__(self):
        self.assets = {"CASH": 0}
        self.deals = []

    def make_deal(self, deal:  Deal):
        self.deals.append(deal)
        if deal.ticker == "CASH":
            self.assets["CASH"] += deal.count
            return
        if deal.ticker.startwith("DIVIDEND_"):
            self.assets["CASH"] += deal.count
            return
        if deal.ticker == "FEE":
            self.assets["CASH"] -= deal.count
            return
        if deal.ticker in self.assets:
            self.assets[deal.ticker] += deal.count
        else:
            self.assets[deal.ticker] = deal.count
        price = deal.count*deal.ticker.get_price(deal.date)
        self.assets["CASH"] -= price
        fee = price*0.0007
        d = deal
        d.ticker = "FEE"
        d.count = fee
        self.make_deal(d)

    def get_value(self, date):
        self.assets.clear()
        for deal in self.deals:
            if deal.date<date:
                self.make_deal(deal)
        value = 0
        for asset in self.assets:
            value += asset.ticker.get_price(date)*asset.count
        return value

