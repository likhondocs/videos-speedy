from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import subprocess

app = Flask(__name__)

# List of directories to scrape for videos
VIDEO_DIRECTORIES = [
    "https://ocean.marcus.pw:8008/RileyReid/%5BSiterip%5D%20Riley%20Reid%20-%20ReidMyLips.com%20%5B2019-12-09%5D/",
    "https://ocean.marcus.pw:8008/JAV/%5BBEB016%5D%20JULIA%20%28Uncensored%20Leak%29%20%5B720p%5D/",
    "https://ocean.marcus.pw:8008/Onlyfans/%5BOnlyFans.com%5D%20Anri%20Okita%20%28%40anriokita_real%29%20%5B2019-02-13%5D/",
    "https://ocean.marcus.pw:8008/Onlyfans/%5BOnlyFans.com%5D%20Daneilley%20Ayala%20%28%40danyellay%29%20%5B2019-12-14%5D/video/",
    "https://ocean.marcus.pw:8008/Packs/%5BPornhubPremium%5D%20Purple%20Bitch%20%5BMegaPack%5D/"
]

# Function to generate thumbnail
def generate_thumbnail(video_url, output_thumbnail):
    try:
        command = ['ffmpeg', '-i', video_url, '-ss', '00:00:10', '-vframes', '1', output_thumbnail]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating thumbnail for {video_url}: {e}")

# Function to scrape video links and generate thumbnails
def fetch_videos_from_directory(directory_url):
    try:
        response = requests.get(directory_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        videos = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('.mp4'):
                video_url = urljoin(directory_url, href)
                thumbnail_url = video_url.replace('.mp4', '.jpg')  # Assume thumbnail follows same URL convention
                videos.append({
                    'name': href.split('/')[-1],
                    'url': video_url,
                    'thumbnail': thumbnail_url
                })
        return videos
    except requests.exceptions.RequestException as e:
        print(f"Error fetching videos from {directory_url}: {e}")
        return []

# Fetch videos from all directories
def fetch_all_videos():
    all_videos = []
    for directory in VIDEO_DIRECTORIES:
        videos = fetch_videos_from_directory(directory)
        all_videos.extend(videos)
    return all_videos

@app.route('/videos', methods=['GET'])
def get_videos():
    videos = fetch_all_videos()
    return jsonify(videos)

@app.route('/')
def index():
    videos = fetch_all_videos()
    return render_template('index.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
