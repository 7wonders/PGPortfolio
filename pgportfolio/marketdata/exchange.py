import json
import time
from datetime import datetime

import ccxt

from pgportfolio.tools.configprocess import preprocess_config

minute = 60
hour = minute * 60
day = hour * 24
week = day * 7
month = day * 30
year = day * 365

valid_periods = {
        300: '5m',
        900: '15m',
        1800: '30m',
        7200: '2h',
        14400: '4h',
        86400: '1d'
    }


class Exchange:
    def __init__(self):
        # load exchange from net_config.json - default poloniex
        with open("pgportfolio/net_config.json") as file:
            config = json.load(file)
        config = preprocess_config(config)
        exchange = config["input"]["exchange"]
        print(exchange)
        self.exchange = getattr(ccxt, exchange)()
        self.exchange.load_markets()
        # Conversions
        self.timestamp_str = lambda timestamp=time.time(), format="%Y-%m-%d %H:%M:%S": datetime.fromtimestamp(
            timestamp).strftime(format)
        self.str_timestamp = lambda datestr=self.timestamp_str(), format="%Y-%m-%d %H:%M:%S": int(
            time.mktime(time.strptime(datestr, format)))
        self.float_roundPercent = lambda floatN, decimalP=2: str(round(float(floatN) * 100, decimalP)) + "%"

        # PUBLIC COMMANDS
        self.marketTicker = lambda x=0: self.exchange.fetch_tickers()
        # self.marketVolume = lambda x=0: self.api('return24hVolume')
        # self.marketStatus = lambda x=0: self.exchange.fetch_markets()
        # self.marketLoans = lambda coin: self.api('returnLoanOrders', {'currency': coin})
        # self.marketOrders = lambda pair='all', depth=10: \
        #     self.api('returnOrderBook', {'currencyPair': pair, 'depth': depth})
        self.marketChart = lambda pair, period=day, start=time.time() - (week * 1), end=time.time(): self.exchange.fetch_ohlcv(pair, timeframe=valid_periods[int(period)], since=int(start * 1000), limit=(datetime.fromtimestamp(end) - datetime.fromtimestamp(start)).days)
        # self.api(
        # 'returnChartData', {'currencyPair': pair, 'period': period, 'start': start, 'end': end})
        # self.marketTradeHist = lambda pair: self.api('returnTradeHistory',
        #                                              {'currencyPair': pair})  # NEEDS TO BE FIXED ON Exchange
