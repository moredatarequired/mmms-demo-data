import os

from dotenv import load_dotenv
from pymongo import MongoClient


def mongodb_connection_string():
    load_dotenv()
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASS")
    base = f"mongodb+srv://{user}:{password}@sandboxcluster0-yoosx.mongodb.net"
    return base + "/test?retryWrites=true&w=majority"


def connect_to_mongodb():
    return MongoClient(mongodb_connection_string())
