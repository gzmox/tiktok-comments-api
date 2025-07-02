from flask import Flask, request, jsonify
from TikTokApi import TikTokApi
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "TikTok Comments API is running."

@app.route("/comments")
async def get_comments():
    url = request.args.get("url", "")
    match = re.search(r'/video/(\d+)', url)
    if not match:
        return jsonify({"error": "Invalid TikTok video URL"}), 400

    try:
        video_id = match.group(1)
        api = TikTokApi()
        video = api.video(id=video_id)
        comments = await asyncio.gather(*[comment async for comment in video.comments(count=30)])
        usernames = [c.author.username for c in comments]
        return jsonify({"usernames": usernames})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
