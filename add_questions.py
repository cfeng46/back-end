import json
from PyMongo import MongoClient

with open('questions.json', encoding="utf8") as data_file:    
    data = json.load(data_file)

client = MongoClient()
db = client.interceptDB
collection = db.questions
collection.insert_many(data)
