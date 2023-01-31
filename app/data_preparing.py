from typing import Optional, List
from datetime import datetime
from pprint import pprint

from tinkoff.invest import CandleInterval, Client, InstrumentIdType
from tinkoff.invest.exceptions import RequestError
from tinkoff.invest.utils import now
import pandas as pd
import numpy as np

from settings import TOKEN, ENVIRONMENT

def stock_prices_download(figi: str, year: int) -> pd.Series:
    """
    Max period for the each request is a year

    figi: The Financial Instrument Global Identifier (FIGI) 
    year: The accounting year

    The function returns close prices
    """
    
    prices_series = pd.Series(
        index=pd.date_range(
            start=datetime(year=year, month=1, day=1),
            end=datetime(year=year, month=12, day=31)
        ).strftime('%m-%d'),
        name=year,
        dtype=float
    )
    with Client(TOKEN, target=ENVIRONMENT) as client:
        info = client.instruments.share_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id=figi
        )
        for candle in client.get_all_candles(
            figi=figi,
            from_=datetime(year=year, month=1, day=1),
            to=datetime(year=year, month=12, day=31),
            interval=CandleInterval.CANDLE_INTERVAL_DAY,
        ):
            prices_series.loc[
                candle.time.date().strftime('%m-%d')
            ] = (
                info.instrument.lot*
                candle.close.units+candle.close.nano/(10**9)
            )
    return prices_series

def find_instrument(query:str, type_:Optional[str]=None):
    """
    query: Company name or fraze to find company by
    type_ (None, 'bond', 'share'...): instrument type

    return: generator 
    """
    with Client(TOKEN) as client:
        instruments = client.instruments.find_instrument(query=query)
        choosen_instruments = []
        if type(type_) is not None:
            for instrument in instruments.instruments:
                if instrument.instrument_type==type_:
                    choosen_instruments.append(instrument)
            return choosen_instruments
        else:
            return instruments

def find_figi_with_info(stock_names: List[str], save_path: str) -> None:
    """
    Get the list with companies tickers

    Save information about instrument [name, instrument's figi]
    """
    stocks_names_figis = []
    for stock_name in stock_names:
        generator = find_instrument(stock_name, 'share')
        if type(generator)==type(None):
            print(stock_name)
            continue
        for company in generator:
            stocks_names_figis.append([company.name, company.figi])
    np.save(f'{save_path}/popular_stocks_figi_name', stocks_names_figis)

def get_historical_prices(
    figis_list: List[List[str]],
    years:  List[int],
    save_path: str
) -> None:
    """
    Get The List with company's name and figi ['name', 'figi']
    years arg is a list obj with account years [2001, 2002 ...]

    Save historical prices as csv files with save path
    """
    for name_figi in figis_list:
        first=True
        try:
            for year in years:  
                if first:
                    prices = stock_prices_download(
                        figi=name_figi[1], 
                        year=year
                    )
                    first=False
                else:
                    prices = pd.concat(
                        [
                            prices,
                            stock_prices_download(
                                figi=name_figi[1], 
                                year=year
                            )
                        ],
                        axis=1
                    )
        except RequestError as e:
            print(e, '\n', name_figi[0])
            continue

        prices.to_csv(
            f'{save_path}/{name_figi[0]}_{name_figi[1]}_{min(years)}_{max(years)}.csv'
        )
