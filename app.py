from flask import Flask, request, jsonify
import re
import asyncio
from scraper import scrape_comments

app = Flask(__name__)

@app.route("/")
def home():
    return "TikTok Comment Scraper is live."

@app.route("/comments")
def comments():
    url = request.args.get("url", "")
    match = re.search(r'/video/(\d+)', url)
    if not match:
        return jsonify({"error": "Invalid TikTok video URL"}), 400
    try:
        users = asyncio.run(scrape_comments(url, limit=30))
        return jsonify({"usernames": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
