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
# create collection
organizations = db.organizations
q = db.questions

# return questions
def get_questions(category_id):
    if tag_is is None:
        return q.find()
    else:
        # implement how to create/retrieve a survey based on tag IDs selected by user
        return q.find({'categoryId': category_id}));
