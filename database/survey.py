import pymongo
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson import json_util
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
app = Flask(__name__)

# connect to the database
client = pymongo.MongoClient("mongodb://admin:intercept@45.55.198.145/interceptDB")
db = client.interceptDB
q = db.questions

# return questions
def get_questions(category_id):
    print('got to heere in surveyyy')
    print(category_id)
    if category_id is None:
        print('should be in here')
        print(q.find())
        return q.find()
    else:
        print('should not be here')
        # implement how to create/retrieve a survey based on category(or tag?) IDs selected by user
        return q.find({'categoryId': category_id})
