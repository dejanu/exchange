#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
from order import Order
from orderbook import OrderBook
from matchingengine import MatchingEngine

app = Flask(__name__)

order_book = OrderBook()
engine = MatchingEngine(order_book)
trades_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def submit_order():
    data = request.json
    try:
        order = Order(data["side"], float(data["price"]), int(data["quantity"]))
        trades = engine.match_order(order)
        if order.quantity > 0 and order.price is not None:
            order_book.add_order(order)
        trades_history.extend(trades)
        msg = f"Order submitted. {len(trades)} trades executed."
        return jsonify({"message": msg})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400

@app.route("/orderbook")
def get_orderbook():
    bids = [(price, sum(o.quantity for o in level.orders)) for price, level in order_book.bids.items()]
    asks = [(price, sum(o.quantity for o in level.orders)) for price, level in order_book.asks.items()]
    return jsonify({"bids": bids, "asks": asks})

@app.route("/trades")
def get_trades():
    return jsonify(trades_history)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
