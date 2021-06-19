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

    def get_price(self, ticker, date):
        sql = """SELECT price.price_close FROM price, ticker 
        WHERE (price.id_ticker=ticker.id_ticker) AND (ticker.ticker=?) AND (price.date=?);"""
        self.cursor.execute(sql, [ticker, date])
        x = self.cursor.fetchall()
        if len(x) > 0:
            price_close = x[0]
            if price_close is not None:
                return price_close[0]
            else:
                return 0
        else:
            return 0

    def add_deal(self, ticker, count, date):
        sql = """SELECT id_ticker FROM ticker WHERE ticker=?;"""
        self.cursor.execute(sql, [ticker])
        id_ticker = self.cursor.fetchone()[0]
        if id_ticker is not None:
            sql = """SELECT price_close, price_magic_time FROM price WHERE id_ticker=?;"""
            self.cursor.execute(sql, [id_ticker])
            x = self.cursor.fetchall()
            if len(x) > 0:
                price_close = x[0][0]
                price_magic_time = x[0][1]
            else:
                price_close = None
                price_magic_time = None
            if price_magic_time is not None:
                sql = """INSERT INTO deal(id_ticker,count,date,price) VALUES (?,?,?,?);"""
                self.cursor.execute(sql, [id_ticker, count, date, price_magic_time])
                self.db.commit()
            else:
                if price_close is not None:
                    sql = """INSERT INTO deal(id_ticker,count,date,price) VALUES (?,?,?,?);"""
                    self.cursor.execute(sql, [id_ticker, count, date, price_close])
                    self.db.commit()
                else:
                    sql = """INSERT INTO deal(id_ticker,count,date,price) VALUES (?,?,?,?);"""
                    self.cursor.execute(sql, [id_ticker, count, date, -1])
                    self.db.commit()

    def get_deals(self):
        sql = """SELECT ticker.ticker, deal.count, deal.date FROM ticker, deal 
        WHERE ticker.id_ticker=deal.id_ticker;"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

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