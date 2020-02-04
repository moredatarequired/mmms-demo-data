from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

db = client.test_database

collection = db.test_collection

import datetime

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow(),
}

posts = db.posts

post_id = posts.insert_one(post).inserted_id

db.list_collection_names()

import pprint

pprint.pprint(posts.find_one())

pprint.pprint(posts.find_one({"_id": post_id}))
