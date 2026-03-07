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
            resting_order = level.pop_order()
            traded_qty = min(order.quantity, resting_order.quantity)
            order.quantity -= traded_qty
            resting_order.quantity -= traded_qty

            trades.append((resting_order.id, order.id, best_price, traded_qty))

            # partial order match: If resting order still has quantity, re-add it to the price level
            if resting_order.quantity > 0:
                level.add_order(resting_order)

            if not level.is_empty():
                opposite[best_price] = level
            else:
                del opposite[best_price]  # remove empty price level

        return trades