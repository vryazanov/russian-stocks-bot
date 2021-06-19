import db


class Ticker:

    def __init__(self, ticker, name=""):
        self.ticker = ticker
        self.name = name
        self.db = db.DB()

    def get_price(self, date):
        if self.ticker == "CASH":
            return 1
        if self.ticker.startswith("DIVIDEND_"):
            return 0
        if self.ticker == "FEE":
            return 0
        return self.db.get_price(self.ticker, date)
