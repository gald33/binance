import time
from consts import C
from signals import Signal
from consts import Settings
from order_core import Order_core


signal = Signal(symbol='ETHBTC',
                buying_low_range=0.10,
                buying_high_range=0.11,
                target_prices=[0.12],
                stop_loss=0.085,
                signal_btc_value=0.01)
for i in xrange(10):
    print 'iteration', i+1
    work_results = signal.work()
    mode = work_results[0]
    if mode == C.sell_mode:
        if len(work_results) > 1:
            order_core = work_results[1]
            order_core.print_order_core()
    time.sleep(Settings.iterations_sleep_time)

# eth_trader  = Symbol_trader(symbol='ETHBTC')
# prices = eth_trader.get_recent_prices()
# sleep = 0.1
# target = Target(target=0.1, stop_loss=0.88, prices=prices)
# order_core = target.new_tick_decision(prices=prices)
# order_core.print_order_core()
# time.sleep(sleep)
# for i in xrange(100):
#     print 'iteration', i+1
#     prices = eth_trader.get_recent_prices()
#     order_core = target.new_tick_decision(prices=prices)
#     order_core.print_order_core()
#     time.sleep(sleep)
#




# pprint(eth_trader.get_open_orders())
# pprint(eth_trader.get_canceled_orders())
# pprint(eth_trader.get_order('49397729'))
# eth_trader.buy_limit(quantity=1, price=0.001)
# eth_trader.cancel_order('51703009')


# get all symbol prices
# trades = client.get_historical_trades(symbol='BNBBTC')
# pprint(trades)


# place a test market buy order, to place an actual order use the create_order function
# order = client.create_test_order(
#     symbol='ETHBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)
# pprint(order)

# orders = client.get_all_orders(symbol='ETHBTC', limit=10)
# pprint(orders)

# info = client.get_symbol_info('BNBBTC')
# pprint(info)





#buy ether
# order = client.order_limit_buy(
#     symbol='ETHBTC',
#     quantity=1,
#     price='0.001')
# pprint(order)
# raw_input('pause')

# check orders
# orders = client.get_all_orders(symbol='ETHBTC', limit=10)
# pprint(orders)

# check specific order
# order = client.get_order(
#     symbol='ETHBTC',
#     orderId='49397729')
# pprint(order)

#cancel order
# result = client.cancel_order(
#     symbol='ETHBTC',
#     orderId='49397729')
# pprint(result)