#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template_string
from order import Order
from orderbook import OrderBook
from matchingengine import MatchingEngine

app = Flask(__name__)

order_book = OrderBook()
engine = MatchingEngine(order_book)
trades_history = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Exchange Demo</title>
    <style>
        body { font-family: Arial; margin: 2em; }
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .order-form { margin-bottom: 2em; }
        .order-book, .trades { margin-top: 2em; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 4px 8px; }
    </style>
</head>
<body>
    <div class="center-container">
        <h1>Exchange Demo</h1>
        <div class="order-form">
            <form id="orderForm">
                <label>Side:
                    <select name="side">
                        <option value="buy">Buy</option>
                        <option value="sell">Sell</option>
                    </select>
                </label>
                <label>Price: <input type="number" step="0.01" name="price" required></label>
                <label>Quantity: <input type="number" name="quantity" required></label>
                <button type="submit">Submit Order</button>
            </form>
            <div id="result"></div>
        </div>
        <div class="order-book">
            <h2>Order Book</h2>
            <div id="orderBook"></div>
        </div>
        <div class="trades">
            <h2>Trade History</h2>
            <div id="trades"></div>
        </div>
    </div>
<script>
function renderOrderBook(data) {
    let html = "<table><tr><th>Bids</th><th>Asks</th></tr>";
    let maxLen = Math.max(data.bids.length, data.asks.length);
    for (let i = 0; i < maxLen; i++) {
        let bid = data.bids[i] || ["", ""];
        let ask = data.asks[i] || ["", ""];
        html += `<tr><td>${bid[0]} (${bid[1]})</td><td>${ask[0]} (${ask[1]})</td></tr>`;
    }
    html += "</table>";
    document.getElementById("orderBook").innerHTML = html;
}
function renderTrades(trades) {
    if (trades.length === 0) {
        document.getElementById("trades").innerHTML = "<em>No trades yet.</em>";
        return;
    }
    let html = "<table><tr><th>#</th><th>Resting Order</th><th>Incoming Order</th><th>Price</th><th>Quantity</th></tr>";
    trades.forEach((t, i) => {
        html += `<tr><td>${i+1}</td><td>${t[0]}</td><td>${t[1]}</td><td>${t[2]}</td><td>${t[3]}</td></tr>`;
    });
    html += "</table>";
    document.getElementById("trades").innerHTML = html;
}
function refresh() {
    fetch("/orderbook").then(r => r.json()).then(renderOrderBook);
    fetch("/trades").then(r => r.json()).then(renderTrades);
}
document.getElementById("orderForm").onsubmit = function(e) {
    e.preventDefault();
    let form = e.target;
    let data = {
        side: form.side.value,
        price: form.price.value,
        quantity: form.quantity.value
    };
    fetch("/order", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(r => r.json()).then(resp => {
        document.getElementById("result").innerText = resp.message;
        refresh();
    });
};
refresh();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/order", methods=["POST"])
def submit_order():
    data = request.json
    try:
        order = Order(data["side"], float(data["price"]), int(data["quantity"]))
        order_book.add_order(order)
        trades = engine.match_order(order)
        trades_history.extend(trades)
        msg = f"Order submitted. {len(trades)} trades executed."
        return jsonify({"message": msg})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400

@app.route("/orderbook")
def get_orderbook():
    bids = [(price, sum(o.quantity for o in level.orders)) for price, level in reversed(order_book.bids.items())]
    asks = [(price, sum(o.quantity for o in level.orders)) for price, level in order_book.asks.items()]
    return jsonify({"bids": bids, "asks": asks})

@app.route("/trades")
def get_trades():
    return jsonify(trades_history)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
