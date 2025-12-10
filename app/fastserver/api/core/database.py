# app/core/database.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        load_dotenv()

        mongo_uri = os.getenv('MONGO_URI')
        if mongo_uri is None:
            raise ValueError("MONGO_URI environment variable is not set")

        mongo_db = os.getenv('MONGO_DB')
        if mongo_db is None:
            raise ValueError("MONGO_DB environment variable is not set")

        self.mongo_uri: str = mongo_uri
        self.mongo_db: str = mongo_db
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print("[MongoDB] Connected to DB:", self.db.name)

    def close(self):
        if self.client:
            self.client.close()

mongodb = MongoDB()

def connect_to_mongo():
    mongodb.connect()

def close_mongo_connection():
    mongodb.close()
