import os

from langchain_core.tools import tool
from newsapi import NewsApiClient

from tools.utils import error_json, to_json, ttl_cache


@ttl_cache(seconds=300)
def fetch_news(query: str, max_items: int, api_key: str) -> dict:
    client = NewsApiClient(api_key=api_key)
    return client.get_everything(q=query, language="en", sort_by="publishedAt",
                                 page=1, page_size=max_items)


@tool
def crypto_news_tool(query: str, max_items: int = 5) -> str:
    """Search recent cryptocurrency news (NewsAPI).

    Args:
        query: Search keywords in English, such as 'bitcoin' or 'ethereum ETF'.
        max_items: Maximum number of articles to return (1-20).
    """
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        return error_json("NEWSAPI_KEY is missing")
    max_items = max(1, min(int(max_items), 20))
    try:
        res = fetch_news(query, max_items, api_key)
        articles = []
        for a in res.get("articles", [])[:max_items]:
            articles.append({
                "title": a.get("title"),
                "source": (a.get("source") or {}).get("name"),
                "url": a.get("url"),
                "publishedAt": a.get("publishedAt"),
                "description": a.get("description"),
            })
        return to_json({
            "status": res.get("status") == "ok",
            "totalResults": res.get("totalResults", 0),
            "returned": len(articles),
            "articles": articles,
        })
    except Exception as e:
        return error_json(str(e))