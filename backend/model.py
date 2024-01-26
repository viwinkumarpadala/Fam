#Iport statements
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

#creating a class for defining the data format
class YouTubeVideo:
    def __init__(self, title, description, published_at, thumbnail, video_id):
        self.title = title
        self.description = description
        self.published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
        self.thumbnail = thumbnail
        self.video_id = video_id

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at,
            'thumbnail': self.thumbnail,
            'video_id': self.video_id
        }
#get the url from dotenv file
db_url=os.getenv('db_url')

# Connect to MongoDB
client = MongoClient(db_url)
db = client['youtube_database']  
collection = db['videos'] 

#sample data to store and check if it is working
data = {
    "description": "PYTHON tutorials by Mr. Vijay Sir.",
    "publishedAt": "2024-01-25T15:06:18Z",
    "thumbnail": "https://i.ytimg.com/vi/xSuY3bfmkR0/default_live.jpg",
    "title": "PYTHON tutorials by Mr. Vijay Sir",
    "videoId": "xSuY3bfmkR0"
}

# Create a YouTubeVideo object
video = YouTubeVideo(
    title=data['title'],
    description=data['description'],
    published_at=data['publishedAt'],
    thumbnail=data['thumbnail'],
    video_id=data['videoId']
)

# Convert the video object to a dictionary
video_data = video.to_dict()

# Insert the video data into MongoDB
insert_result = collection.insert_one(video_data)

# Succesfully created the object Hehehehe...