"""Portfolio related services."""
import collections
import datetime
import decimal
import typing

import injector

from bot.services.deal import Deal
from bot.services.ticker import Ticker


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
        self.assets = {"CASH": 0}
        for deal in self.deals:
            if deal.date<date:
                self.make_deal(deal)
        value = 0
        for t, c in self.assets:
            ticker = Ticker(t)
            value += ticker.get_price(date)*c
        return value
