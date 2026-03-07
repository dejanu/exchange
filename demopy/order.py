from collections import deque
import itertools

# unique order id generator
order_id_counter = itertools.count(1)

class Order:
    def __init__(self, side, price, quantity):
        """Initialize an order with a unique ID, side, price, and quantity."""
        self.id = next(order_id_counter)  # Generate a unique order ID
        self.side = side  #  determines which side of book to match  'buy' or 'sell'
        self.price = price # None for market orders
        self.quantity = quantity