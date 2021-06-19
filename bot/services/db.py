import sqlite3
import csv


class DB:

    def __init__(self):
        self.db = sqlite3.connect("db.db")
        self.cursor = self.db.cursor()

    def import_price(self, ticker, filename):
        sql = """SELECT id_ticker FROM ticker WHERE ticker=?;"""
        self.cursor.execute(sql, [ticker])
        id_ticker = self.cursor.fetchone()[0]
        if id_ticker is not None:
            with open(filename, newline='') as file:
                prices = csv.DictReader(file)
                for price in prices:
                    sql = """SELECT date FROM price WHERE id_ticker=?;"""
                    self.cursor.execute(sql, [id_ticker])
                    date = (x[0] for x in self.cursor.fetchall())
                    if (price["Date"] is not None) and \
                            (price["Open"] is not None) and \
                            (price["Close"] is not None) and \
                            (price["Date"] not in date):
                        sql = """INSERT INTO price(id_ticker,date,price_open,price_close) VALUES (?,?,?,?);"""
                        self.cursor.execute(sql, [id_ticker, price["Date"], price["Open"], price["Close"]])
                        self.db.commit()


        # sql = """SELECT id_ticker FROM ticker WHERE name=?"""
        # self.cursor.execute(sql, [ticker])
        # id_ticker = self.cursor.fetchone()
        # date = "01.01.2021"
        # price_open = 1.1
        # price_close = 1.2
        # price_magic_time = 1.3
        # sql = """INSERT INTO price VALUES (?,?,?,?,?)"""
        # self.cursor.execute(sql, [id_ticker, date, price_open, price_close, price_magic_time])
        # self.db.commit()


# db = DB()
# db.import_price("GAZP", "D://Capitalist Club//Эксперимент//Стоимость портфелей//GAZP.txt")
# db.import_price("GMKN", "D://Capitalist Club//Эксперимент//Стоимость портфелей//GMKN.txt")
# db.import_price("HYDR", "D://Capitalist Club//Эксперимент//Стоимость портфелей//HYDR.txt")
# db.import_price("LKOH", "D://Capitalist Club//Эксперимент//Стоимость портфелей//LKOH.txt")
# db.import_price("MAGN", "D://Capitalist Club//Эксперимент//Стоимость портфелей//MAGN.txt")
# db.import_price("MGNT", "D://Capitalist Club//Эксперимент//Стоимость портфелей//MGNT.txt")
# db.import_price("MOEX", "D://Capitalist Club//Эксперимент//Стоимость портфелей//MOEX.txt")
# db.import_price("NLMK", "D://Capitalist Club//Эксперимент//Стоимость портфелей//NLMK.txt")
# db.import_price("SBER", "D://Capitalist Club//Эксперимент//Стоимость портфелей//SBER.txt")
# db.import_price("SBERP", "D://Capitalist Club//Эксперимент//Стоимость портфелей//SBERP.txt")
# db.import_price("SNGSP", "D://Capitalist Club//Эксперимент//Стоимость портфелей//SNGSP.txt")

