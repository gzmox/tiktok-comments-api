from flask import Flask, request, jsonify
from TikTokApi import TikTokApi
import re

app = Flask(__name__)

@app.route('/comments')
def get_comments():
    url = request.args.get("url", "")
    match = re.search(r'/video/(\d+)', url)
    if not match:
        return jsonify({"error": "Invalid TikTok video URL"}), 400

    video_id = match.group(1)

    try:
        api = TikTokApi()
        video = api.video(id=video_id)
        comments = video.comments(count=30)
        usernames = [comment.author.username for comment in comments]
        return jsonify({"usernames": usernames})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
