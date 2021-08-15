import db


class Deal:

    def __init__(self, ticker, count, date):
        self.ticker = ticker
        self.count = count
        self.date = date
        self.db = db.DB()

    def add_deal(self):
        self.db.add_deal(self.ticker, self.count, self.date)


# d = Deal("CASH", 6091.4*10, "2021-02-01")
# d.add_deal()
# d = Deal("CASH", 6091.4, "2021-02-01")
# d.add_deal()
# d = Deal("CASH", 6091.4, "2021-03-01")
# d.add_deal()
# d = Deal("CASH", 6091.4, "2021-04-01")
# d.add_deal()
# d = Deal("CASH", 6091.4, "2021-05-01")
# d.add_deal()
# d = Deal("CASH", 6091.4, "2021-06-01")
# d.add_deal()
# d = Deal("LKOH", 1, "2021-02-01")
# d.add_deal()
# d = Deal("SBER", 20, "2021-02-01")
# d.add_deal()
# d = Deal("SBERP", 20, "2021-02-01")
# d.add_deal()
# d = Deal("MOEX", 30, "2021-02-01")
# d.add_deal()
# d = Deal("GAZP", 20, "2021-02-01")
# d.add_deal()
# d = Deal("GMKN", 1, "2021-03-01")
# d.add_deal()
# d = Deal("HYDR", 7000, "2021-03-01")
# d.add_deal()
# d = Deal("GAZP", 20, "2021-03-01")
# d.add_deal()
# d = Deal("GAZP", 20, "2021-04-01")
# d.add_deal()
# d = Deal("SBERP", 20, "2021-05-04")
# d.add_deal()
# d = Deal("MOEX", 30, "2021-05-04")
# d.add_deal()
# d = Deal("GAZP", 20, "2021-05-04")
# d.add_deal()
