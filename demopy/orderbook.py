from collections import defaultdict
from sortedcontainers import SortedDict  # pip install sortedcontainers
from price import PriceLevel

class OrderBook:
    def __init__(self):
        self.bids = SortedDict(lambda x: -x)  # descending for best bid
        self.asks = SortedDict()              # ascending for best ask

    def add_order(self, order):
        book = self.bids if order.side == "buy" else self.asks
        price = order.price
        if price not in book:
            book[price] = PriceLevel()
        book[price].add_order(order)

    def __str__(self):
        result = "Order Book:\nBids:\n"
        for price, level in self.bids.items():
            total_qty = sum(order.quantity for order in level.orders)
            result += f"  Price: {price}, Quantity: {total_qty}\n"
        result += "Asks:\n"
        for price, level in self.asks.items():
            total_qty = sum(order.quantity for order in level.orders)
            result += f"  Price: {price}, Quantity: {total_qty}\n"
        return result