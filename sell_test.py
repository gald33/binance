from target import Target_handler
from pprint import pprint

target_handler = Target_handler()
pprint(target_handler.targets)
for i in xrange(1, 2):
    order_core = target_handler.work()
    order_core.print_order_core()
