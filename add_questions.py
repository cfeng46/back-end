import json
from PyMongo import MongoClient

with open('updated_current_questions.json', encoding="utf8") as data_file:
    data = json.load(data_file)

client = pymongo.MongoClient("mongodb://admin:intercept@45.55.198.145/interceptDB")
db = client.interceptDB
collection = db.questions
collection.insert_many(data)
