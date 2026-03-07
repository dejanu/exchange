#!/usr/bin/env python3

from order import Order
from orderbook import OrderBook
from matchingengine import MatchingEngine

# Initialize
order_book = OrderBook()
engine = MatchingEngine(order_book)

# Add some limit orders
order_book.add_order(Order('buy', price=100, quantity=5))
order_book.add_order(Order('sell', price=105, quantity=3))
order_book.add_order(Order('sell', price=106, quantity=3))

# Simulate a new incoming order
incoming_order = Order('buy', price=105, quantity=2)
trades = engine.match_order(incoming_order)

# Print trades in a user-friendly format
if not trades:
    print("No trades were executed.")
else:
    print("Executed trades:")
    for i, (resting_order_id, incoming_order_id, price, quantity) in enumerate(trades, start=1):
        print(
            f"  {i}. Resting Order #{resting_order_id} matched with "
            f"Incoming Order #{incoming_order_id} | "
            f"Price: {price} | Quantity: {quantity}"
        )

# Print order book state
print(order_book)