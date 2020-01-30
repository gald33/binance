from enum import Enum


class C(Enum):
    limit_on_upper_is_optimal = 1
    limit_on_lower_is_optimal = 2
    buy_mode = 3
    sell_mode = 4
    waiting_for_seller = 5
    waiting_for_buyer = 6



class Settings:
    trader_sleep_time = 0.1
    iterations_sleep_time = 1
