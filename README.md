comp684-demo — Shopping Cart Service (demo)

Overview
--------
A small, in-memory Python shopping cart service with unit tests. This repository contains a simple `ShoppingCart` class (in `src/shopping_cart.py`) with methods to add/remove items and compute the cart total. Tests are in `tests/test_shopping_cart.py` and were validated with `pytest`.

Notes / Known behaviors
----------------------
- Items are stored in-memory as a dict: `item_id -> {"quantity": int, "price": float}`.
- Adding an existing item increases quantity but does not update the stored price (this is a deliberate current behavior and may be changed later).
- Removing more quantity than exists deletes the item (no negative quantities are possible).
- No persistence or concurrency control is implemented.

Run locally (Windows PowerShell)
-------------------------------
1. Create and activate a virtual environment (if you don't already have one):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run tests:

```powershell
python -m pytest -v
```

What I pushed
--------------
- `src/shopping_cart.py` — ShoppingCart implementation
- `tests/test_shopping_cart.py` — pytest tests (7 passing tests)
- `requirements.txt` — pytest deps
- `README.md` — this file

Next suggested improvements
-------------------------
- Decide and document price-update semantics when adding the same item with different prices.
- Add serialization (to/from dict or JSON) and a `clear()` method.
- Consider custom exception types for clearer error handling.
- Add concurrency/locking or move to a per-request cart when used in a web service.

If you'd like, I can:
- Push a follow-up commit that enforces a price-update rule (e.g., reject price mismatches or update the price using a weighted average) and add tests for it.
- Create a small web API wrapper (Flask/FastAPI) around this cart for manual testing.

Repository remote: https://github.com/Arian-D/comp684-demo