import os

import requests
from langchain_core.tools import tool

from tools.utils import error_json, http_get_json, to_json, ttl_cache

API_URL = "https://api.freecryptoapi.com/v1/getCryptoList"


@ttl_cache(seconds=600)
def fetch_crypto_list(token: str) -> list:
    data = http_get_json(API_URL, headers={"Authorization": f"Bearer {token}"})
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        found = data.get("data") or data.get("result") or data.get("cryptocurrencies") or []
        return found if isinstance(found, list) else []
    return []


@tool
def crypto_list_tool(limit: int = 25) -> str:
    """Retrieve a list of cryptocurrencies (symbol and name) from FreeCryptoAPI.

    Args:
        limit: Maximum number of cryptocurrencies to return (1-200).
    """
    token = os.getenv("FREECRYPTO_TOKEN")
    if not token:
        return error_json("FREECRYPTO_TOKEN is missing")
    limit = max(1, min(int(limit), 200))
    try:
        coins = fetch_crypto_list(token)
    except requests.exceptions.RequestException as e:
        return error_json(str(e))

    result = []
    for coin in coins[:limit]:
        if isinstance(coin, dict):
            result.append({
                "symbol": coin.get("symbol") or coin.get("Symbol") or coin.get("ticker"),
                "name": coin.get("name") or coin.get("Name"),
            })
    return to_json(result)