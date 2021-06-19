import db


class Deal:

    def __init__(self, ticker, count, date):
        self.ticker = ticker
        self.count = count
        self.date = date
        self.db = db.DB()

    def add_deal(self):
        self.db.add_deal(self.ticker, self.count, self.date)




# d1 = Deal("CASH", 1000, "2020-05-21")
# d1.add_deal()
# d2 = Deal("SBER", 10, "2020-05-21")
# d2.add_deal()
