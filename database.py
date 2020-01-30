
class Database_handler:
    def __init__(self):
        self.db = self.get_db()

    def get_db(self):
        from pymongo import MongoClient
        client = MongoClient('localhost:27017')
        db = client.binance
        return db

    def save_target(self, target):  # saves initial target data (not recent data)
        result = self.db.targets.insert_one(
            {
                'target' : target.target,
                'stop_loss' : target.initial_stop_loss,
                'buying_price' : target.buying_price,
                'quantity' : target.quantity,
                'symbol' : target.trader.symbol
            }
        )

    def load_targets(self):
        from target import Target
        targets = []
        cursor = self.db.targets.find({})
        for target in cursor:
            targets.append(Target(target=target['target'],
                                  stop_loss=target['stop_loss'],
                                  buying_price=target['buying_price'],
                                  quantity=target['quantity'],
                                  symbol=target['symbol'])
                           )
        return targets
