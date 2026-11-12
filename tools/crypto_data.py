import os

import requests
from langchain_core.tools import tool

from tools.utils import error_json, http_get_json, to_json, ttl_cache

API_URL = "https://api.freecryptoapi.com/v1/getData"


@ttl_cache()
def fetch_market_data(symbol: str, token: str) -> dict:
    return http_get_json(API_URL, headers={"Authorization": f"Bearer {token}"},
                         params={"symbol": symbol})


@tool
def crypto_data_tool(symbol: str) -> str:
    """Retrieve current market data (price, volume, change...) for ONE cryptocurrency.

    Args:
        symbol: Cryptocurrency ticker such as BTC, ETH or BNB.
    """
    token = os.getenv("FREECRYPTO_TOKEN")
    if not token:
        return error_json("FREECRYPTO_TOKEN is missing")
    symbol = symbol.upper().strip()
    if not symbol.isalnum():
        return error_json(f"Invalid symbol: {symbol!r}")
    try:
        return to_json(fetch_market_data(symbol, token))
    except requests.exceptions.RequestException as e:
        return error_json(str(e))