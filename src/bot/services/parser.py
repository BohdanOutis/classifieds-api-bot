from typing import List, Dict, Any
import hashlib
import feedparser

import httpx

def generate_md5(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

async def fetch_fresh_news(api_client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    response = await api_client.get("/news")
    sources = response.json() if response.status_code == 200 else []
    fresh_news = []

    for source in sources:
        feed = feedparser.parse(source['url'])

        for entry in feed.entries:
            link = entry.get("link", "")
            title = entry.get("title", "")
            description = entry.get("summary", "")

            if not link:
                continue

            news_hash = generate_md5(link)


            if not await api_client.get("/processed_news", params={"news_hash": news_hash}):
                fresh_news.append({
                    "source_id": source['id'],
                    "source_name": source['name'],
                    "title": title,
                    "link": link,
                    "description": description,
                    "hash": news_hash
                })

    return fresh_news