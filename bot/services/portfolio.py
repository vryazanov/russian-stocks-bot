"""Portfolio related services."""
import db
import deal
import ticker


class Portfolio:

    def __init__(self):
        self.assets = {"CASH": 0}
        self.deals = []
        self.db = db.DB()

    def make_deal(self, d):
        self.deals.append(d)
        if d.ticker == "CASH":
            return
        if d.ticker.startswith("DIVIDEND_"):
            return
        t = ticker.Ticker(d.ticker)
        price = d.count * t.get_price(d.date)
        fee = 0.0007 * price
        if d.ticker is not "FEE":
            x = deal.Deal("FEE", fee, d.date)
            self.make_deal(x)

    def calc_deal(self, d):
        if d.ticker == "CASH":
            self.assets["CASH"] += d.count
            return
        if d.ticker.startswith("DIVIDEND_"):
            self.assets["CASH"] += d.count
            return
        if d.ticker == "FEE":
            self.assets["CASH"] -= d.count
            return
        if d.ticker in self.assets:
            self.assets[d.ticker] += d.count
        else:
            self.assets[d.ticker] = d.count
        t = ticker.Ticker(d.ticker)
        price = d.count*t.get_price(d.date)
        self.assets["CASH"] -= price
        return

    def get_deals(self):
        self.deals.clear()
        for d in self.db.get_deals():
            self.make_deal(deal.Deal(d[0], d[1], d[2]))
        return

    def get_value(self, date):
        self.get_deals()
        self.assets.clear()
        self.assets = {"CASH": 0}
        for d in self.deals:
            if d.date < date:
                self.calc_deal(d)
        value = 0
        for tick in self.assets:
            t = ticker.Ticker(tick)
            value += t.get_price(date)*self.assets[tick]
        return value


p = Portfolio()
print(p.get_value("2021-04-12"))
print(p.get_value("2021-04-21"))
