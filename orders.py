import re
from binance.enums import SIDE_BUY, SIDE_SELL

VALID_SIDES = {"BUY": SIDE_BUY, "SELL": SIDE_SELL}

def validate_symbol(symbol: str):
    # Basic validation: uppercase alphanumeric
    if not re.match(r'^[A-Z0-9]+USDT$', symbol):
        raise ValueError("Symbol must be of form <ASSET>USDT, uppercase, e.g., BTCUSDT")
    return symbol

def validate_side(side: str):
    side_up = side.upper()
    if side_up not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL")
    return VALID_SIDES[side_up]

def validate_quantity(qty: str):
    try:
        val = float(qty)
        if val <= 0:
            raise ValueError
        return val
    except:
        raise ValueError("Quantity must be a positive number")

def validate_price(price: str):
    try:
        val = float(price)
        if val <= 0:
            raise ValueError
        return val
    except:
        raise ValueError("Price must be a positive number")