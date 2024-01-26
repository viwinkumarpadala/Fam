# Import statements
from celery import Celery
from pymongo import MongoClient
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

# Initializing Celery application
app = Celery('tasks', broker='amqp://viwin:kumar@rabbitmq:5672//')


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

# Defining a celery task, that works Asynchronously and updates the database every 10 seconds 
@app.task
def fetch_and_store_videos():
    # We are using the same function as in the server, but here for the purpose of caching, we are using cricket as a fixed search query 
    published_after = datetime(2023, 1, 1)

    published_after_str = published_after.isoformat() + 'Z'

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    #For caching we are getting 20 responses every time so that the first page can be filled with that data

    search_response = youtube.search().list(
        q='cricket',
        type='video',
        order='date',
        publishedAfter=published_after_str,
        part='snippet',
        maxResults=20  
    ).execute()

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
    #Sort the videos in reverse chronological order
    videos.sort(key=lambda x: x['publishedAt'], reverse=True)
    # Insert videos into the database
    #Here we are iterating the response and if it doesn't exist in it, then we will push it into db, or else break the loop
    for video in videos:
        video_id = video['videoId']
        existing_video = collection.find_one({'videoId': video_id})
        if not existing_video:
            collection.insert_one(video)
        else:
            break  

# Schedule the task to run every 10 seconds
app.conf.beat_schedule = {
    'fetch-videos-every-10-seconds': {
        'task': 'tasks.fetch_and_store_videos',  # Note: Use the module path to refer to the task
        'schedule': 10.0,
    },
}


# from celery import Celery
# from celery.schedules import crontab

# app = Celery('tasks', broker='amqp://viwin:kumar@rabbitmq:5672//')

# app.conf.beat_schedule = {
#     'task-name': {
#         'task': 'tasks.print_message',
#         'schedule': 10.0,  # Run every 10 seconds
#     },
# }

# @app.task
# def print_message():
#     text='hello'
#     print(text)
