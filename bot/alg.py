import math


quotes = {
    'SBER': {
        'price': 244,
        'lot': 10,
    },
    'GAZP': {
        'price': 212,
        'lot': 10,
    },
    'LKOH': {
        'price': 5238,
        'lot': 1,
    },
}


def buy(steak_cost: int, steaks: int, tickers: list):
    result = []

    for ticker in tickers:
        lot_price = quotes[ticker]['price'] * quotes[ticker]['lot']

        if lot_price < steak_cost:
            steaks_needed = 1
        else:
            steaks_needed = math.ceil(lot_price / steak_cost)

        if steaks_needed > steaks:
            # no enough funds to buy this ticker
            break

        lots_to_buy = (steaks_needed * steak_cost) // lot_price

        stocks_to_buy = lots_to_buy * quotes[ticker]['lot']
        cost = stocks_to_buy * quotes[ticker]['price']

        
        steaks -= steaks_needed

        result.append({'ticker': ticker, 'stocks': steak_cost, 'cost': cost})

    return result


results = buy(10000, 2, ['SBER', 'LKOH', 'GAZP'])

for result in results:
    ticker, stocks, cost = result['ticker'], result['stocks'], result['cost']
    print(f'Buy {stocks} stocks of {ticker} for {cost} rubles.')