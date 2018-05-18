from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from datetime import datetime

import pandas as pd

from pgportfolio.constants import *
from pgportfolio.marketdata.exchange import Exchange
from pgportfolio.tools.data import get_chart_until_success


class CoinList(object):
    def __init__(self, end, volume_average_days=1, volume_forward=0):
        self._exchange = Exchange()
        # connect the internet to accees volumes
        ticker = self._exchange.marketTicker()
        pairs = []
        coins = []
        volumes = []
        prices = []

        logging.info("select coin online from %s to %s" % (datetime.fromtimestamp(end - (DAY * volume_average_days) -
                                                                                  volume_forward).
                                                           strftime('%Y-%m-%d %H:%M'),
                                                           datetime.fromtimestamp(end - volume_forward).
                                                           strftime('%Y-%m-%d %H:%M')))
        for k, v in ticker.items():
            if k.endswith("/BTC"):
                pairs.append(k)
                coins.append(k.split('/')[0])
                prices.append(float(v['last']))
                volumes.append(self.__get_total_volume(
                    pair=k,
                    global_end=end,
                    days=volume_average_days,
                    forward=volume_forward)
                )
        print(pairs)
        print(coins)
        self._df = pd.DataFrame({'coin': coins, 'pair': pairs, 'volume': volumes, 'price': prices})
        self._df = self._df.set_index('coin')

    @property
    def allActiveCoins(self):
        return self._df

    # @property
    # def allCoins(self):
    #     return self._exchange.marketStatus().keys()

    @property
    def exchange(self):
        return self._exchange

    def get_chart_until_success(self, pair, start, period, end):
        return get_chart_until_success(self._exchange, pair, start, period, end)

    # get several days volume
    def __get_total_volume(self, pair, global_end, days, forward):
        start = global_end - (DAY * days) - forward
        end = global_end - forward
        chart = self.get_chart_until_success(pair=pair, period=DAY, start=start, end=end)
        result = 0
        for one_day in chart:
            result += one_day[5]
        return result

    def topNVolume(self, n=5, order=True, minVolume=0):
        if minVolume == 0:
            r = self._df.loc[self._df['price'] > 2e-6]
            r = r.sort_values(by='volume', ascending=False)[:n]
            print(r)
            if order:
                return r
            else:
                return r.sort_index()
        else:
            return self._df[self._df.volume >= minVolume]
