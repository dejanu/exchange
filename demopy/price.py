
from collections import deque

class PriceLevel:
    """ Price levels as a queue """
    def __init__(self):
        self.orders = deque() # FIFO queue for time priority

    def add_order(self, order):
        self.orders.append(order)
    
    def pop_order(self):
        return self.orders.popleft()
    
    def is_empty(self):
        return len(self.orders) == 0
    