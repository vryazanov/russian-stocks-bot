import requests

from bot.storage import PurchaseStorage


token = '6071b1161ae602.16550571'
ticker = 'SBERP'
exchange = 'MCX'

params = {
    'from': '2021-01-01',
    'to': '2021-04-01',
    'api_token': token,
    'prediod': 'd',
}


def fetch(purchases: PurchaseStorage, token: str):
    """Fetch historical quotes for all tickers."""
    tickers = set()

    for purchase in purchases.all():
        for stock in purchase.stocks:
            tickers.add(stock.name)

    print(tickers)
    # url = 'https://eodhistoricaldata.com/api/eod/{ticker}.{exchange}'.format(
    #     ticker=ticker,
    #     exchange=exchange,
    # )
    # response = requests.get(url, params=params)
