import datetime


class Ticker:

    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name

    def get_price(self, date: datetime.date):
        if self.ticker == "CASH":
            return 1
        if self.ticker.startswith("DIVIDEND_"):
            return 0
        if self.ticker == "FEE":
            return 0
        return -1
