from TikTokApi import TikTokApi
import json
import re

def handler(request, response):
    try:
        query = request.get("queryStringParameters", {})
        url = query.get("url", "")
        match = re.search(r'/video/(\d+)', url)
        if not match:
            return response(
                400,
                body=json.dumps({"error": "Invalid TikTok video URL"}),
                headers={"Content-Type": "application/json"}
            )

        video_id = match.group(1)

        # Initialize API
        api = TikTokApi()
        video = api.video(id=video_id)

        # Fetch comments
        comments = video.comments(count=30)
        usernames = [comment.author.username for comment in comments]

        return response(
            200,
            body=json.dumps({"usernames": usernames}),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return response(
            500,
            body=json.dumps({"error": str(e)}),
            headers={"Content-Type": "application/json"}
        )
