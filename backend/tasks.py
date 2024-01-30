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
# creating index on the field publishedAt
collection.create_index([('publishedAt', -1)])

# Getting the youtube api key from .env file
API_KEY = os.getenv('api_key')
API_KEY2 = os.getenv('api_key2')
API_KEY3 = os.getenv('api_key3')
API_KEY4 = os.getenv('api_key4')
API_KEY5 = os.getenv('api_key5')

#Handling the case for having multiple keys, and use an alternative key, if one of them is null
API_KEY = API_KEY or API_KEY2 or API_KEY3 or API_KEY4 or API_KEY5
# list of api keys that can be used when rate limitation is happened
API_KEYS=[API_KEY, API_KEY2, API_KEY3, API_KEY4, API_KEY5]
# Defining a celery task, that works Asynchronously and updates the database every 10 seconds 
@app.task
def fetch_and_store_videos():
    published_after = datetime(2023, 1, 1)
    published_after_str = published_after.isoformat() + 'Z'
    #run a loop to avoid rate limitation error by using multiple keys
    for key in API_KEYS:
        try:
            youtube = build('youtube', 'v3', developerKey=key)
            
            search_response = youtube.search().list(
                q='cricket',
                type='video',
                order='date',
                publishedAfter=published_after_str,
                part='snippet',
                maxResults=60
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

            videos.sort(key=lambda x: x['publishedAt'], reverse=True)

            for video in videos:
                video_id = video['videoId']
                existing_video = collection.find_one({'videoId': video_id})
                if not existing_video:
                    collection.insert_one(video)
                else:
                    break  # Stop inserting if video already exists
            break  # Stop trying other keys if successful
        except:
            continue  # If key fails, try the next one


# Schedule the task to run every 10 seconds
app.conf.beat_schedule = {
    'fetch-videos-every-10-seconds': {
        'task': 'tasks.fetch_and_store_videos',  
        'schedule': 10.0,
    },
}

