import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
# Base URL override for futures testnet
testnet_base_url = 'https://testnet.binancefuture.com'

# Validate keys
if not API_KEY or not API_SECRET:
    raise ValueError("Please set API_KEY and API_SECRET in environment variables or .env file")
