from binance.client import Client
import key
from pprint import pprint
import time
from consts import Settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Client(key.key, key.secret) # connection to binance
# db = Database_handler() # local mongodb db

class Symbol_trader:
    def __init__(self, symbol):
        logger.debug('<Symbol_trader.__init__>')
        self.symbol = symbol
        self.num_of_retrieved_orders = 10 # parameter
        self.prices = []
        self.sleep = Settings.trader_sleep_time    #to avoid bans
        self.live = False    # TODO: need to add this in buys or sells, False means testing

    def get_recent_prices(self):    #updates recent symbol prices, and returns it
        logger.debug('<Symbol_trader.get_recent_prices>')
        trades = client.get_recent_trades(symbol=self.symbol)
        # Some info:
        # print 'len of history', len(trades)
        # print 'first'
        # pprint(trades[0])
        # print 'last'
        # pprint(trades[-1])
        time.sleep(self.sleep)
        self.prices = []
        for trade in trades:
            self.prices.append(float(trade[u'price']))
        return self.prices

    def get_opens(self):    #returns opens
        logger.debug('<Symbol_trader.get_opens>')
        opens = []
        timestamps = []
        trades = client.get_historical_klines(
            symbol=self.symbol,
            interval=Client.KLINE_INTERVAL_1DAY,
            start_str="1 Dec, 2017")
        # Some info:
        # print 'len of history', len(trades)
        # print 'first'
        # pprint(trades[0])
        # print 'last'
        # pprint(trades[-1])
        # time.sleep(self.sleep)
        # self.prices = []
        for trade in trades:
            opens.append(float(trade[1]))
            timestamps.append(trade[0])
        return opens, timestamps

    def get_orders(self):
        orders = client.get_all_orders(symbol=self.symbol, limit=self.num_of_retrieved_orders)
        print 'Retrieved', self.num_of_retrieved_orders, 'last orders:'
        return orders

    def get_open_orders(self):
        orders = self.get_orders()
        open_orders = []
        for order in  orders:
            if order['status'] == 'NEW':
                open_orders.append(order)
        return open_orders

    def get_canceled_orders(self):
        orders = self.get_orders()
        open_orders = []
        for order in  orders:
            if order['status'] == 'CANCELED':
                open_orders.append(order)
        return open_orders

    def get_filled_orders(self):
        orders = self.get_orders()
        open_orders = []
        for order in  orders:
            if order['status'] == 'FILLED':
                open_orders.append(order)
        return open_orders

    def get_order(self, order_id):    # check specific order
        order = client.get_order(symbol=self.symbol, orderId=order_id)
        return order

    def is_order_open(self, order_id):
        order = self.get_order(order_id)
        if order['status'] == 'NEW':
            return True
        else:
            return False

    def is_order_canceled(self, order_id):
        order = self.get_order(order_id)
        if order['status'] == 'CANCELED':
            return True
        else:
            return False

    def is_order_filled(self, order_id):
        order = self.get_order(order_id)
        if order['status'] == 'FILLED':
            buying_price = float(order[u'price'])
            return True, buying_price
        else:
            return False, None

    def _buy_limit_without_check(self, quantity, price):   # don't use externally, instead use method with checks
        if self.live:
            order = client.order_limit_buy(
                symbol=self.symbol,
                quantity=quantity,
                price=price)
            print 'order'
            pprint(order)
            print 'buy', self.symbol, quantity, price
            return order
        else:
            print 'buy', self.symbol, quantity, price, '- not live'
            return {'orderId':'not_live'}

    def buy_limit(self, quantity, price):
        order = self._buy_limit_without_check(quantity=quantity, price=price)
        if self.live:
            is_order_open = self.is_order_open(order['orderId'])
            print 'is order open'
            print is_order_open
        else:
            is_order_open = True
            print 'is order open'
            print is_order_open, '- not live'
        if is_order_open:
            return is_order_open, order['orderId']  # true, order_id
        else:
            return is_order_open, None  # false, order_id


    def _cancel_order_without_check(self, order_id):    #call only from 'cancel_order()'
        if self.live:
            result = client.cancel_order(
                symbol=self.symbol,
                orderId=order_id)
        print 'results:'
        pprint(result)
        return result

    def cancel_order(self, order_id):
        result = self._cancel_order_without_check(order_id=order_id)
        is_order_canceled = self.is_order_canceled(order_id=order_id)
        print 'is_order_canceled'
        print is_order_canceled
        return is_order_canceled
