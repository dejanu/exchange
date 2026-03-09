class MatchingEngine:
    def __init__(self, order_book):
        self.book = order_book

    def match_order(self, order):
        trades = []

        if order.side == "buy":
            opposite = self.book.asks
        else:
            opposite = self.book.bids

        while order.quantity > 0 and opposite:
            best_price = opposite.peekitem(0)[0]
            if order.price is not None:  # limit order
                if (order.side == "buy" and order.price < best_price) or \
                   (order.side == "sell" and order.price > best_price):
                    break  # cannot match
            # else: market order or price allows match

            level = opposite[best_price]
            if level.is_empty():
                del opposite[best_price]
                continue

            resting_order = level.orders[0]
            if resting_order.quantity <= 0:
                level.pop_order()
                if level.is_empty():
                    del opposite[best_price]
                continue

            traded_qty = min(order.quantity, resting_order.quantity)
            if traded_qty <= 0:
                break

            order.quantity -= traded_qty
            resting_order.quantity -= traded_qty

            trades.append((resting_order.id, order.id, best_price, traded_qty))

            if resting_order.quantity == 0:
                level.pop_order()

            if level.is_empty():
                del opposite[best_price]  # remove empty price level

        return trades