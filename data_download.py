import numpy as np

from app.data_preparing import get_historical_prices

years = [2000+x for x in range(23)]
figis_list = np.load('data/popular_stocks_figi_name.npy')

if __name__ == "__main__":
    get_historical_prices(figis_list, years, 'data/stocks')
