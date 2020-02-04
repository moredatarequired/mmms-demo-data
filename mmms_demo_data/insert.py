from datetime import datetime
from pprint import pprint

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.benchmark_db
collection = db.test_collection

n = 1000000

profiles = [
    {
        "member_id": "0-14-023267-" + str(i),
        "address": "862 Kayla Courts Suite 344\nHenrymouth, TX 45885",
        "birthdate": datetime(1998, 1, 21),
        "mail": "obrienkyle@yahoo.com",
        "name": "Rebecca White",
        "policies": ["978-0-85681-845-5"],
        "sex": "F",
        "ssn": "495-08-2662",
    }
    for i in range(n)
]

start = datetime.now()
# for p in profiles:
#     collection.insert_one(p)
collection.insert_many(profiles)
print(f"inserted {n} in {datetime.now() - start}")

db.list_collection_names()
pprint(collection.find_one())
