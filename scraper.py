import json
from typing import List
import httpx
from parsel import Selector

async def scrape_comments(video_url: str, limit: int = 50) -> List[str]:
    async with httpx.AsyncClient(http2=True, headers={
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
                      "AppleWebKit/537.36 (KHTML, like Gecko) "+
                      "Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br"
    }) as client:
        resp = await client.get(video_url)
        if resp.status_code != 200:
            raise Exception("Blocked or failed request")

        sel = Selector(resp.text)
        script = sel.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        if not script:
            return []

        data = json.loads(script)
        comments_data = (
            data.get("props", {})
                .get("pageProps", {})
                .get("awemeDetail", {})
                .get("comments", {})
                .get("comments", [])
        )

        users = []
        for item in comments_data:
            username = item.get("user", {}).get("uniqueId")
            if username and username not in users:
                users.append(username)
            if len(users) >= limit:
                break

        return users
