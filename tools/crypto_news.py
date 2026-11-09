import os
import json
from dotenv import load_dotenv
from newsapi import NewsApiClient
from langchain_core.tools import tool

load_dotenv()


@tool
def crypto_news_tool(query: str, max_items: int = 5) -> str:
    """
    Search recent cryptocurrency news using NewsAPI.

    Args:
        query: Search keywords, such as bitcoin or ethereum.
        max_items: Maximum number of articles to return.

    Returns:
        A JSON string containing article titles, sources, URLs
        and publication dates.
    """
    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        return json.dumps({
            "status": False,
            "error": "NEWSAPI_KEY is missing"
        })

    try:
        newsapi = NewsApiClient(api_key=api_key)

        max_items = max(1, min(max_items, 100))

        res = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page=1,
            page_size=max_items
        )

        articles = []

        for article in res.get("articles", [])[:max_items]:
            source_info = article.get("source") or {}

            articles.append({
                "title": article.get("title"),
                "source": source_info.get("name"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "description": article.get("description")
            })

        result = {
            "status": res.get("status") == "ok",
            "totalResults": res.get("totalResults", 0),
            "returned": len(articles),
            "articles": articles
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "status": False,
            "error": str(e)
        })