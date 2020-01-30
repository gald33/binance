from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Order_core:
    def __init__(self, upper_price, lower_price, stop, optimal_limit_rule):
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.stop = stop
        self.optimal_limit_rule = optimal_limit_rule

    def print_order_core(self):
        # print 'upper_price, lower_price, stop, optimal_limit_rule'
        logger.info(str(datetime.now()) + ': upper: ' + str(self.upper_price) + ', lower: ' + str(self.lower_price) + \
            ', stop: ' + str(self.stop) + ', rule: ' + str(self.optimal_limit_rule))
