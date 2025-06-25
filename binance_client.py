from binance import Client
import logging

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, testnet=True):
        # Initialize client
        self.client = Client(api_key, api_secret, testnet=testnet)
        if testnet:
            # Override futures base URL for testnet
            # According to python-binance, passing testnet=True sets correct endpoints for futures testnet
            # But if needed, override manually:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
        logging.debug(f"Initialized Binance Futures client (testnet={testnet})")

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logging.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing market order: {e}")
            raise

    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce=time_in_force,
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing limit order: {e}")
            raise

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price, time_in_force='GTC'):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                stopPrice=stop_price,
                price=limit_price,
                timeInForce=time_in_force,
                quantity=quantity
            )
            logging.info(f"Stop-Limit order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing stop-limit order: {e}")
            raise