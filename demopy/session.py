#!/usr/bin/env python3

from order import Order
from orderbook import OrderBook
from matchingengine import MatchingEngine

# Initialize
order_book = OrderBook()
engine = MatchingEngine(order_book)

# Add some limit orders
#order_book.add_order(Order('buy', price=100, quantity=5))
order_book.add_order(Order('sell', price=102, quantity=4))
order_book.add_order(Order('sell', price=104, quantity=3))

# Simulate a new incoming order
def print_trades(trades):
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

def print_order_book():
    print("\nOrder Book:")
    print("Bids:")
    for price, level in order_book.bids.items():
        qty = sum(order.quantity for order in level.orders)
        print(f"  Price: {price} | Quantity: {qty}")
    print("Asks:")
    for price, level in order_book.asks.items():
        qty = sum(order.quantity for order in level.orders)
        print(f"  Price: {price} | Quantity: {qty}")
    print()

def main():
    print("Exchange Server Started. Enter orders (buy/sell) or 'exit' to quit.")
    print ("Example input: 'buy 101 10' or 'sell 99 5'")
    while True:
        cmd = input("Order (buy/sell) [side price quantity] or 'exit': ").strip()
        if cmd.lower() == 'exit':
            break
        try:
            side, price, quantity = cmd.split()
            price = float(price)
            quantity = int(quantity)
            order = Order(side, price=price, quantity=quantity)
            trades = engine.match_order(order)
            if order.quantity > 0 and order.price is not None:
                order_book.add_order(order)
            print_trades(trades)
            print_order_book()
        except Exception as e:
            print(f"Invalid input or error: {e}")

if __name__ == "__main__":
    main()