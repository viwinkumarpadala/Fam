#Import statements

from flask import Flask, jsonify, request
from pymongo import MongoClient
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

db_url = os.getenv('db_url')
client = MongoClient(db_url)
db = client['youtube_database']
collection = db['videos']

# Getting the youtube api key from .env file
API_KEY = os.getenv('api_key')
API_KEY2 = os.getenv('api_key2')
API_KEY3 = os.getenv('api_key3')
API_KEY4 = os.getenv('api_key4')
API_KEY5 = os.getenv('api_key5')

#Handling the case for having multiple keys, and use an alternative key, if one of them not works
API_KEY = API_KEY or API_KEY2 or API_KEY3 or API_KEY4 or API_KEY5

# Function to fetch videos from YouTube API using a search query( for the search bar feature)
def fetch_videos_from_youtube(query):
    # Taking only the latest videos after date 01/01/2023
    published_after = datetime(2023, 1, 1)

    published_after_str = published_after.isoformat() + 'Z'

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Getting 100 responses in youtube api so that we can use that for pagination 20 videos per page
    search_response = youtube.search().list(
        q=query,
        type='video',
        order='date',
        publishedAfter=published_after_str,
        part='snippet',
        maxResults=100 
    ).execute()

    # Create an array for storing the videos data from the response
    videos = []
    for item in search_response['items']:
        video = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'publishedAt': item['snippet']['publishedAt'],
            'thumbnail': item['snippet']['thumbnails']['default']['url'],
            'videoId': item['id']['videoId']
        }
        videos.append(video)
    #This is sorted to maintain the reverse chronological order in the response
    videos.sort(key=lambda x: x['publishedAt'], reverse=True)
    return videos

# GET route for getting the videos for the search bar functionality
@app.route('/videos')
def get_videos_from_youtube():
    query = request.args.get('query')
    page = int(request.args.get('page', 1))  
    #default page number=1
    per_page = 20
    #20 videos per page
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    videos = fetch_videos_from_youtube(query)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_videos = videos[start_index:end_index]
    #paginating the response and returning them
    return jsonify({'videos': paginated_videos})

# GET route for getting the cached data( the data that we have been caching asynchornously using Rabbitmq and Celery)
@app.route('/videos/cached')
def get_videos_from_cache_or_youtube():
    page = int(request.args.get('page', 1))  
    per_page = 20  
    # Reverse chronological order
    cached_videos = list(collection.find().sort('publishedAt', -1))  

    if cached_videos:
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_videos = cached_videos[start_index:end_index]

        # Convert ObjectId to string for JSON serialization
        for video in paginated_videos:
            video['_id'] = str(video['_id'])

        return jsonify({'videos': paginated_videos})
    else:
        query = 'cricket'  # Cricket is used as a fixed search query 
        videos = fetch_videos_from_youtube(query)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_videos = videos[start_index:end_index]
        return jsonify({'videos': paginated_videos})

if __name__ == '__main__':
    app.run(debug=True)
