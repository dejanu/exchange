# Demo Exchange App

## High-Level Description

This project implements a basic exchange backend in Python.  
It consists of four main components:

- **Order** (`order.py`): Represents individual buy or sell orders.
- **PriceLevel** (`price.py`): Manages a queue of orders at a specific price.
- **OrderBook** (`orderbook.py`): Stores and organizes bids and asks using efficient sorted data structures.
- **MatchingEngine** (`matchingengine.py`): Handles the core logic for matching incoming orders against the order book and generating trades.

The design uses efficient data structures (`SortedDict`, `deque`) to ensure fast order insertion, retrieval, and matching.  
This forms the foundation for a simple, performant exchange suitable for demo and educational purposes.

The current implementation allows trading a single asses. The order class does not implement a symbol filed and no separate order books are implemented currently.

---

* Cmds

```bash
# venv stuff
python -m venv .demovevn
source .demovevn/bin/activate

# start interactive session in terminal
./session.py

# start interactive session in browser
./web.py

# docker
docker run -p 5000:5000 dejanualex/exchange:1.0
```