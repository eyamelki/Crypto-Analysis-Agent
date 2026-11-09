import os
import json
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def crypto_data_tool(symbol: str) -> str:
    """
    Retrieve market data for one cryptocurrency from FreeCryptoAPI.

    Args:
        symbol: Cryptocurrency symbol, such as BTC, ETH or BNB.

    Returns:
        A JSON string containing the cryptocurrency market data.
    """
    token = os.getenv("FREECRYPTO_TOKEN")

    if not token:
        return json.dumps({
            "status": False,
            "error": "FREECRYPTO_TOKEN is missing"
        })

    url = "https://api.freecryptoapi.com/v1/getData"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "symbol": symbol.upper().strip()
    }

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        resp.raise_for_status()
        data = resp.json()

        return json.dumps(data, indent=2)

    except requests.exceptions.RequestException as e:
        return json.dumps({
            "status": False,
            "error": str(e)
        })

    except ValueError:
        return json.dumps({
            "status": False,
            "error": "Invalid JSON from API"
        })