from binance.client import Client
from binance.enums import *
import numpy as np

import key
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import finance

from indicators import *

sma_handler = Sma_handler()

from pprint import pprint
from datetime import datetime

client = Client(key.key, key.secret)

# products = client.get_products()
# depth = client.get_order_book(symbol='TRXBTC')
candles = client.get_klines(symbol='TRXBTC', interval=KLINE_INTERVAL_1DAY)
# candles = client.get_klines(symbol='TRXBTC', interval=KLINE_INTERVAL_30MINUTE)

opentimes = []
opens = []
highs = []
lows = []
closes = []


for candle in candles:
    opentimes.append(candle[0])
    opens.append(float(candle[1]))
    highs.append(float(candle[2]))
    lows.append(float(candle[3]))
    closes.append(float(candle[4]))

### take last points
# numOfPoints = 70
# del opentimes[:numOfPoints]
# del opens[:numOfPoints]
# del highs[:numOfPoints]
# del lows[:numOfPoints:]
# del closes[:numOfPoints:]



peak_handler = Peak_handler(highs)
# if too many peaks with count 2 or more, limit the number of samples
max_values, min_value = peak_handler.find_peaks(100, 0.05)
max_lines = peak_handler.find_lines(0)

def plot_lines(lines, original_list):
    for line in lines:
        plt.plot(peak_handler.line_to_list(line, original_list))
# plot_lines(max_lines, highs)

# can ref original list in max_values somehow later
def plot_max_or_min_values(peaks, original_list, minimum_count):
    for peak in peaks:
        if peak.count >= minimum_count:
            plt.plot(peak_handler.value_to_list(peak.value, original_list))
# plot_max_or_min_values(max_values, highs, 3)


# for peak in max_values:
#     print peak.value, peak.count, peak.high - peak.low
# print len(max_values)
#
# first_max_list = value_to_list(peak.low, highs)
# pprint(first_max_list)
# print len(first_max_list), len(highs)
# plt.plot(first_max_list)

# sma_50 = sma_handler.sma(closes, 50)
# sma_100 = sma_handler.sma(closes, 100)



# fig1 = plt.plot(sma_50)#, 'b', opentimes, highs, 'r^', opentimes, lows, 'g*', opentimes, opens, 'y')
# fig2 = plt.plot(sma_100)#, 'b', opentimes, highs, 'r^', opentimes, lows, 'g*', opentimes, opens, 'y')


########
### plot
###closes
# fig = plt.plot(closes)#, 'b', opentimes, highs, 'r^', opentimes, lows, 'g*', opentimes, opens, 'y')
### axis
ax = plt.axes()
ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
### candles
finance.candlestick2_ochl(ax, opens, closes, highs, lows, width=0.4, colorup='g', colordown='r', alpha=0.75)
plt.show()
########