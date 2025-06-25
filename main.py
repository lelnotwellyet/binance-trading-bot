import argparse
import sys
import logging
from config import API_KEY, API_SECRET
from binance_client import BinanceFuturesClient
from orders import validate_symbol, validate_side, validate_quantity, validate_price
from logger_setup import setup_logging


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Simplified Binance Futures Trading Bot CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Market order parser
    market_parser = subparsers.add_parser('market', help='Place market order')
    market_parser.add_argument('--symbol', required=True, help='Trading pair symbol, e.g., BTCUSDT')
    market_parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='BUY or SELL')
    market_parser.add_argument('--quantity', required=True, help='Order quantity')

    # Limit order parser
    limit_parser = subparsers.add_parser('limit', help='Place limit order')
    limit_parser.add_argument('--symbol', required=True, help='Trading pair symbol, e.g., BTCUSDT')
    limit_parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='BUY or SELL')
    limit_parser.add_argument('--quantity', required=True, help='Order quantity')
    limit_parser.add_argument('--price', required=True, help='Limit price')

    # Stop-Limit parser
    stop_parser = subparsers.add_parser('stop', help='Place stop-limit order')
    stop_parser.add_argument('--symbol', required=True, help='Trading pair symbol, e.g., BTCUSDT')
    stop_parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='BUY or SELL')
    stop_parser.add_argument('--quantity', required=True, help='Order quantity')
    stop_parser.add_argument('--stop_price', required=True, help='Stop trigger price')
    stop_parser.add_argument('--limit_price', required=True, help='Limit price when triggered')

    # Status check parser
    status_parser = subparsers.add_parser('status', help='Check order status')
    status_parser.add_argument('--symbol', required=True, help='Trading pair symbol, e.g., BTCUSDT')
    status_parser.add_argument('--order_id', required=True, help='Order ID to check')

    args = parser.parse_args()

    # Initialize client
    try:
        bot = BinanceFuturesClient(API_KEY, API_SECRET, testnet=True)
    except Exception as e:
        logging.error(f"Failed to initialize Binance client: {e}")
        sys.exit(1)

    # Common validations (for all except 'status')
    if args.command != 'status':
        try:
            symbol = validate_symbol(args.symbol)
            side = validate_side(args.side)
            quantity = validate_quantity(args.quantity)
        except Exception as e:
            logging.error(f"Validation error: {e}")
            sys.exit(1)
    else:
        try:
            symbol = validate_symbol(args.symbol)
        except Exception as e:
            logging.error(f"Validation error: {e}")
            sys.exit(1)

    # Execute based on command
    try:
        if args.command == 'market':
            result = bot.place_market_order(symbol, side, quantity)
        elif args.command == 'limit':
            price = validate_price(args.price)
            result = bot.place_limit_order(symbol, side, quantity, price)
        elif args.command == 'stop':
            stop_p = validate_price(args.stop_price)
            limit_p = validate_price(args.limit_price)
            result = bot.place_stop_limit_order(symbol, side, quantity, stop_p, limit_p)
        elif args.command == 'status':
            order_id = int(args.order_id)
            result = bot.client.futures_get_order(symbol=symbol, orderId=order_id)
        else:
            logging.error("Unknown command")
            sys.exit(1)
        print("Order response:")
        print(result)
    except Exception as e:
        logging.error(f"Order execution failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
