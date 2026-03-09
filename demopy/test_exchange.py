import unittest

from matchingengine import MatchingEngine
from order import Order
from orderbook import OrderBook


class ExchangeEngineTests(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook()
        self.engine = MatchingEngine(self.book)

    def _book_residual_limit(self, order):
        if order.quantity > 0 and order.price is not None:
            self.book.add_order(order)

    def test_no_match_non_crossing_limits(self):
        """
        Test that non-crossing limit orders do not match and are added to the book.
        """
        self.book.add_order(Order("sell", 101, 5))
        incoming = Order("buy", 100, 5)

        trades = self.engine.match_order(incoming)
        self._book_residual_limit(incoming)

        self.assertEqual(trades, [])
        self.assertEqual(incoming.quantity, 5)
        self.assertIn(100, self.book.bids)
        self.assertIn(101, self.book.asks)

    def test_full_match_exact_quantity(self):
        """
        Test that a limit order fully matches a resting order with the exact quantity.
        """
        resting = Order("sell", 100, 5)
        self.book.add_order(resting)
        incoming = Order("buy", 100, 5)

        trades = self.engine.match_order(incoming)
        self._book_residual_limit(incoming)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0][0], resting.id)
        self.assertEqual(trades[0][2], 100)
        self.assertEqual(trades[0][3], 5)
        self.assertEqual(incoming.quantity, 0)
        self.assertEqual(len(self.book.asks), 0)
        self.assertEqual(len(self.book.bids), 0)

    def test_partial_fill_incoming_larger(self):
        """
        Test that a limit order partially fills a resting order when the incoming order quantity is larger.
        """
        self.book.add_order(Order("sell", 100, 3))
        incoming = Order("buy", 100, 5)

        trades = self.engine.match_order(incoming)
        self._book_residual_limit(incoming)

        self.assertEqual(sum(t[3] for t in trades), 3)
        self.assertEqual(incoming.quantity, 2)
        self.assertIn(100, self.book.bids)
        self.assertEqual(sum(o.quantity for o in self.book.bids[100].orders), 2)

    def test_partial_fill_resting_larger(self):
        """
        Test that a limit order partially fills a resting order when the resting order quantity is larger.
        """
        resting = Order("sell", 100, 10)
        self.book.add_order(resting)
        incoming = Order("buy", 100, 4)

        trades = self.engine.match_order(incoming)

        self.assertEqual(sum(t[3] for t in trades), 4)
        self.assertEqual(incoming.quantity, 0)
        self.assertIn(100, self.book.asks)
        self.assertEqual(self.book.asks[100].orders[0].id, resting.id)
        self.assertEqual(self.book.asks[100].orders[0].quantity, 6)

    def test_fifo_priority_same_price(self):
        """
        Test that orders at the same price are matched in FIFO order.
        """
        first = Order("sell", 100, 3)
        second = Order("sell", 100, 3)
        self.book.add_order(first)
        self.book.add_order(second)

        trades = self.engine.match_order(Order("buy", 100, 4))

        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0][0], first.id)
        self.assertEqual(trades[0][3], 3)
        self.assertEqual(trades[1][0], second.id)
        self.assertEqual(trades[1][3], 1)

    def test_best_price_priority_across_levels(self):
        """
        Test that orders are matched based on the best price across different price levels.
        """
        self.book.add_order(Order("sell", 100, 5))
        self.book.add_order(Order("sell", 99, 2))

        trades = self.engine.match_order(Order("buy", 101, 4))

        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0][2], 99)
        self.assertEqual(trades[0][3], 2)
        self.assertEqual(trades[1][2], 100)
        self.assertEqual(trades[1][3], 2)

    def test_market_order_sweeps_book(self):
        """Test that a market order matches against the book until it is fully filled or the book is exhausted.
        """
        self.book.add_order(Order("sell", 100, 2))
        self.book.add_order(Order("sell", 101, 2))
        incoming = Order("buy", None, 3)

        trades = self.engine.match_order(incoming)

        self.assertEqual(len(trades), 2)
        self.assertEqual(trades[0][2], 100)
        self.assertEqual(trades[0][3], 2)
        self.assertEqual(trades[1][2], 101)
        self.assertEqual(trades[1][3], 1)
        self.assertEqual(incoming.quantity, 0)
        self.assertEqual(sum(o.quantity for o in self.book.asks[101].orders), 1)

    def test_market_order_empty_opposite_side(self):
        """
        Test that a market order with no opposite side liquidity does not execute and remains unfilled.
        """
        incoming = Order("buy", None, 5)

        trades = self.engine.match_order(incoming)

        self.assertEqual(trades, [])
        self.assertEqual(incoming.quantity, 5)
        self.assertEqual(len(self.book.asks), 0)

    def test_invalid_side_current_behavior_routes_to_bids_path(self):
        """
        Test that an order with an invalid side is currently routed to the bids path.
        """
        self.book.add_order(Order("buy", 100, 1))
        incoming = Order("hold", 100, 1)

        trades = self.engine.match_order(incoming)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0][2], 100)


if __name__ == "__main__":
    unittest.main()
