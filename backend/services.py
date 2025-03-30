import requests

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

def get_crypto_price(crypto: str):
    response = requests.get(f"{BINANCE_API_URL}?symbol={crypto.upper()}USDT")
    if response.status_code == 200:
        return float(response.json()["price"])
    return None
