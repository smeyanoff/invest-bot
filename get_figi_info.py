import numpy as np

from app.data_preparing import find_figi_with_info


if __name__ == "__main__":
    with open('data/popular_stocks', 'r') as f:
        stocks = f.read()
    stocks = [x for x in stocks.split('\n')][:-1]
    find_figi_with_info(stocks, 'data')
