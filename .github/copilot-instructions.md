# Copilot Instructions for Exchange Demo Repo

## Project Overview

This repository implements a demo exchange matching engine in Python.  
Core logic includes order creation, price level management, order book handling, and order matching.

## Key Files

- [`demopy/order.py`](demopy/order.py): Defines the [`Order`](demopy/order.py) class for buy/sell/market orders.
- [`demopy/price.py`](demopy/price.py): Implements [`PriceLevel`](demopy/price.py) for queueing orders at a price.
- [`demopy/orderbook.py`](demopy/orderbook.py): Contains [`OrderBook`](demopy/orderbook.py) for managing bids and asks.
- [`demopy/matchingengine.py`](demopy/matchingengine.py): Provides [`MatchingEngine`](demopy/matchingengine.py) for matching incoming orders.
- [`demopy/session.py`](demopy/session.py): Handles trading session logic.
- [`demopy/requirements.txt`](demopy/requirements.txt): Python dependencies (e.g., `sortedcontainers`).

## Coding Guidelines

- Use existing classes and functions for exchange logic.
- Prefer referencing workspace symbols (e.g., [`Order`](demopy/order.py), [`OrderBook`](demopy/orderbook.py)).
- When suggesting code, use Markdown code blocks with language and file path.
- Link referenced symbols and files using fully qualified paths.

## Example Symbol References

- [`Order`](demopy/order.py)
- [`PriceLevel`](demopy/price.py)
- [`OrderBook`](demopy/orderbook.py)
- [`MatchingEngine`](demopy/matchingengine.py)

## Example File References

- [demopy/order.py](demopy/order.py)
- [demopy/orderbook.py](demopy/orderbook.py)
- [demopy/requirements.txt](demopy/requirements.txt)

## Response Format

- Use Markdown formatting.
- Start code blocks with four backticks and language.
- Add file path comments for code changes.
- Use KaTeX for math equations.

## Additional Notes

- Ignore files in [`demopy/.demovevn/`](demopy/.demovevn/) and [`demopy/__pycache__/`](demopy/__pycache__/).
- Do not reference external libraries unless listed in [`demopy/requirements.txt`](demopy/requirements.txt).
