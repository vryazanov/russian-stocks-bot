import sqlite3


class DB:

    def __init__(self):
        self.db = sqlite3.connect("db.db")
        self.cursor = self.db.cursor()

    def import_price(self, ticker, file):
        sql = """SELECT id_ticker FROM ticker WHERE name=?"""
        self.cursor.execute(sql, [ticker])
        id_ticker = self.cursor.fetchone()
        date = "01.01.2021"
        price_open = 1.1
        price_close = 1.2
        price_magic_time = 1.3
        sql = """INSERT INTO price VALUES (?,?,?,?,?)"""
        self.cursor.execute(sql, [id_ticker, date, price_open, price_close, price_magic_time])
        self.db.commit()