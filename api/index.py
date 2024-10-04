import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# URL of the video directory
VIDEO_DIR_URL = "https://ocean.marcus.pw:8008/RileyReid/%5BSiterip%5D%20Riley%20Reid%20-%20ReidMyLips.com%20%5B2019-12-09%5D/"

# Function to scrape and return video URLs from the directory
def fetch_videos():
    try:
        response = requests.get(VIDEO_DIR_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        videos = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('.mp4'):
                video_url = VIDEO_DIR_URL + href
                videos.append({
                    'name': href,
                    'url': video_url
                })
        return videos
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/videos', methods=['GET'])
def get_videos():
    videos = fetch_videos()
    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
