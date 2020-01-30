import numpy as np
from consts import C
from traders import Symbol_trader
from order_core import Order_core
from database import Database_handler
from pprint import pprint

db = Database_handler() # local mongodb db


class Target:
    def __init__(self, target, stop_loss, buying_price, quantity, symbol):
        self.buying_price = buying_price
        self.quantity = quantity    #isn't used internally by a function
        self.trader = Symbol_trader(symbol)    #used after loading
        self.num_of_periods = 10    # how many recent price read to calculate latest price average
        self.target = target    #upper price to sell near, issued as sell limit order - input number
        self.initial_stop_loss = stop_loss  #lower price to sell near, issued as sell limit order with slightly higher stop - input number
        self.greed_factor = 0.01    # parameter, 0 is greedy. how much to sell below target
        self.set_upper_price()
        self.set_initial_lower_price()
        self.initiate_trail_factor = 0.5 # how much from buy price to sell limit before start trailing
        self.trailing_factor = 0.1  # how much lower the sell stop loss limit from latest price average - how much volatility to endure
        self.stop_to_lower_limit_factor = 0.01   # how much above the limit is the stop
        self.closeness_to_limit_switch_factor = 0.7 # e.g. 0.7 means that if upper limit is 3 and lower limit is 2 then if the price >= 2.7 then upper limit is in effect, otherwise stop-loss is in effect
        self.is_trailing = False #initial value
        self.is_sold = False    #relevant for the selling part in target_handler
        self.prices = []
        self.latest_price = None


    def new_tick_decision(self, prices):
        self._set_price_average_internal(prices=prices) # make sure to input enough prices to __init__
        self.set_trailing_rule()
        self.set_lower_price()
        self.set_stop()
        self.set_optimal_limit_rule() # sell limit order should be open on upper price or on lower price
        return Order_core(self.upper_price, self.lower_price, self.stop, self.optimal_limit_rule)

    def set_upper_price(self):
        self.upper_price = self.target * (1 - self.greed_factor)    # TODO: need to add checks so order would fit exchange rules in all prices and stops

    def set_initial_lower_price(self):
        self.lower_price = self.initial_stop_loss * (1 - self.greed_factor)

    def set_lower_price(self):
        if self.is_trailing:
            suggested_lower_price = self.latest_price_average * (1 - self.trailing_factor)
            if suggested_lower_price > self.lower_price:    # lower price can only rise
                self.lower_price = suggested_lower_price

    def set_stop(self):
        self.stop = self.lower_price * (1 + self.stop_to_lower_limit_factor)

    def _set_price_average_internal(self, prices):  #call only from 'set_optimal_limit_rule()'
        latest_prices = prices[-self.num_of_periods:]
        self.latest_price_average = np.mean(latest_prices)

    def set_trailing_rule(self):    # should start trailing?
        if not self.is_trailing:    #once trailing don't stop, check whether to start
            if self.latest_price_average >= self.upper_price * self.initiate_trail_factor + self.buying_price * \
                    (1 - self.initiate_trail_factor):
                self.is_trailing = True
            else:
                self.is_trailing = False

    def set_optimal_limit_rule(self):   # should be upper or lower?
        if self.latest_price_average >= self.upper_price * self.closeness_to_limit_switch_factor + self.lower_price * \
                (1 - self.closeness_to_limit_switch_factor):
            self.optimal_limit_rule = C.limit_on_upper_is_optimal
        else:
            self.optimal_limit_rule = C.limit_on_lower_is_optimal


class Target_handler:
    def __init__(self):
        self.targets = self.load_targets()

    def load_targets(self):
        unfiltered_targets = db.load_targets()
        targets = {}    # symbol is key
        for target in unfiltered_targets:
            if target.trader.symbol not in targets:
                targets[target.trader.symbol] = [] #start a new pair symbol
            targets[target.trader.symbol].append(target)
        return targets

    def work(self): # run once every call, to follow sell orders
        # later replace the choice probabilities to weights of from targets (need to define those), currently it's uniform
        # another approach is do all the targets after updating prices
        symbol = np.random.choice(self.targets.keys(), 1)[0]

        # change the what's in this and the next func
        return self._work_on_selling(symbol)

    def _work_on_selling(self, symbol):  # call only from 'work()'
        # later replace the choice probabilities to weights of from targets (need to define those), currently it's uniform
        # another approach is do all the targets after updating prices (if so, place prices and latest price somewhere better)
        target = np.random.choice(self.targets[symbol], 1)[0]
        target.prices = target.trader.get_recent_prices()  # price read
        target.latest_price = target.prices[-1]  # latest price read
        order_core = target.new_tick_decision(prices=target.prices) #work on one target
        return order_core
