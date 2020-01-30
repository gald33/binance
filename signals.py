import numpy as np
from consts import C
from target import Target
from traders import Symbol_trader
from database import Database_handler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
db = Database_handler() # local mongodb db
from order_core import Order_core


class Signal:
    def __init__(self, symbol, buying_low_range, buying_high_range, target_prices, stop_loss, signal_btc_value):
        logger.debug('<Signal.__init__>')
        self.mode = C.buy_mode  # what do do in 'work()'
        self.buying_order_id = None
        self.selling_order_id = None
        self.buying_price = None
        self.trader = Symbol_trader(symbol=symbol)
        self.buying_low_range = buying_low_range
        self.buying_high_range = buying_high_range
        self.prices = None
        self.latest_price = None
        self.target_prices = target_prices  # list
        self.stop_loss = stop_loss
        self.signal_btc_value = signal_btc_value
        self.targets = []

    def select_quantities(self):
        num_of_targets = len(self.target_prices)
        # decision: currently quantities are divided equally between targets
        quantities = []
        for target_price in self.target_prices:
            btc_value = self.signal_btc_value / num_of_targets
            quantity = round(btc_value / self.latest_price, 2)
            quantities.append(quantity)
        return quantities

    def set_targets(self):
        for i in xrange(len(self.target_prices)):
            target = Target(target=self.target_prices[i], stop_loss=self.stop_loss, buying_price=self.buying_price,
                            quantity=self.quantities[i], symbol=self.trader.symbol)
            # self.targets.append(target)   #signal is created before save, but not used. used only after load
            db.save_target(target)

    def work(self): # run once every call, either wait for buy order to be filled or follow sell orders
        self.prices = self.trader.get_recent_prices()  # price read
        self.latest_price = self.prices[-1]  # latest price read
        if self.mode == C.buy_mode:
            self._work_on_buying()
            return [self.mode]
        elif self.mode == C.waiting_for_seller:
            self._work_on_waiting_for_seller()
            return [self.mode]
        elif self.mode == C.sell_mode:
            return [self.mode, self._work_on_selling()]

    def _work_on_buying(self):  # call only from 'work()'. send buy limit order on the latest price
        logger.debug('<Signal._work_on_buying>')
        if self.latest_price >=self.buying_low_range and self.latest_price <= self.buying_high_range:   #buy if within range
            self.quantities = self.select_quantities()  #depends on latest price
            self.buying_quantity = np.sum(self.quantities)
            success, self.buying_order_id = self.trader.buy_limit(quantity=self.buying_quantity, price=self.latest_price)
            if success:
                self.mode = C.waiting_for_seller
        else:
            print 'price', self.latest_price, 'not in range ['+str(self.buying_low_range)+','\
                                              +str(self.buying_high_range)+'], did not buy'

    def _work_on_waiting_for_seller(self):
        if self.trader.live:
            success, self.buying_price = self.trader.is_order_filled(order_id=self.buying_order_id)
        else:
            success = True
            self.buying_price = self.latest_price
        if success:
            self.set_targets()  # after getting a price when buy order is filled
            self.mode = C.sell_mode

    def _work_on_selling(self):  # call only from 'work()'
        #later replace the choice probabilities to weights of from targets (need to define those), currently it's uniform
        #another approach is do all the targets after updating prices
        target = np.random.choice(self.targets, 1)[0]
        order_core = target.new_tick_decision(prices=self.prices) #work on one target
        return order_core
