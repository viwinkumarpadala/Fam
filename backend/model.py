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
        self.published_at = published_at
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
# creating index on the field published_at
collection.create_index([('published_at', -1)])
