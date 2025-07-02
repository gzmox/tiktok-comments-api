import asyncio
import json
from typing import List, Dict
from httpx import AsyncClient, Response
from parsel import Selector

# Browser-like headers to reduce blocking
client = AsyncClient(http2=True, headers={
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
                  "AppleWebKit/537.36 (KHTML, like Gecko) "+
                  "Chrome/96.0.4664.110 Safari/537.36",
})

async def parse_comments_from_page(response: Response) -> List[str]:
    assert response.status_code == 200, "Blocked or failed"
    sel = Selector(response.text)
    script = sel.xpath("//script[@id='__NEXT_DATA__']/text()").get()
    if not script:
        return []
    data = json.loads(script)
    # Path may vary; this example uses nested structure
    comments = []
    for item in data.get("props", {}).get("pageProps", {}) \
                   .get("awemeDetail", {}) \
                   .get("comments", {}).get("comments", []):
        author = item.get("user", {}).get("uniqueId")
        if author:
            comments.append(author)
    return comments

async def scrape_comments(video_url: str, limit: int = 50) -> List[str]:
    resp = await client.get(video_url)
    all_users = await parse_comments_from_page(resp)
    # Deduplicate and limit
    seen = []
    for u in all_users:
        if u not in seen:
            seen.append(u)
        if len(seen) >= limit:
            break
    return seen
