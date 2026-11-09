
import os
import json
from dotenv import load_dotenv
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
@tool
def crypto_list_tool(limit: int = 25) -> str:
    """
    Retrieve a list of cryptocurrencies from FreeCryptoAPI.
    Returns cryptocurrency symbols and names as JSON.
    """
    token = os.getenv("FREECRYPTO_TOKEN")

    if not token:
        return json.dumps({"error": "FREECRYPTO_TOKEN is missing"})

    url = "https://api.freecryptoapi.com/v1/getCryptoList"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        # Normalize the API response
        if isinstance(data, list):
            cryptocurrencies = data
        elif isinstance(data, dict):
            cryptocurrencies = (
                data.get("data")
                or data.get("result")
                or data.get("cryptocurrencies")
                or []
            )
        else:
            cryptocurrencies = []

        if not isinstance(cryptocurrencies, list):
            return json.dumps(data)

        result = []

        for coin in cryptocurrencies[:limit]:
            if isinstance(coin, dict):
                result.append({
                    "symbol": (
                        coin.get("symbol")
                        or coin.get("Symbol")
                        or coin.get("ticker")
                    ),
                    "name": (
                        coin.get("name")
                        or coin.get("Name")
                    )
                })

        return json.dumps(result, indent=2)

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": str(e)})

    except ValueError:
        return json.dumps({"error": "Invalid JSON response from API"})
