
import os
import json
import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient

# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

FREECRYPTO_TOKEN = os.getenv("FREECRYPTO_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not FREECRYPTO_TOKEN:
    raise ValueError("FREECRYPTO_TOKEN is missing from .env")

if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY is missing from .env")


# ==========================================
# 2. FREECRYPTOAPI - GET CRYPTO LIST
# ==========================================

print("\n========== TEST 1: CRYPTO LIST ==========")

url = "https://api.freecryptoapi.com/v1/getCryptoList"

headers = {
    "Authorization": f"Bearer {FREECRYPTO_TOKEN}"
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    print(json.dumps(data, indent=4))

except requests.exceptions.RequestException as e:
    print("Crypto List API Error:", e)


# ==========================================
# 3. FREECRYPTOAPI - GET BITCOIN DATA
# ==========================================

print("\n========== TEST 2: BITCOIN DATA ==========")

url = "https://api.freecryptoapi.com/v1/getData"

params = {
    "symbol": "BTC"
}

try:
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    print(json.dumps(data, indent=4))

except requests.exceptions.RequestException as e:
    print("Crypto Data API Error:", e)


# ==========================================
# 4. NEWSAPI - GET BITCOIN NEWS
# ==========================================

print("\n========== TEST 3: BITCOIN NEWS ==========")

try:
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    news = newsapi.get_everything(
        q="bitcoin",
        language="en",
        sort_by="relevancy",
        page=1
    )

    print(json.dumps(news, indent=4))

except Exception as e:
    print("NewsAPI Error:", e)


print("\n========== ALL TESTS FINISHED ==========")
