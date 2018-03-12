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
questions = db.questions
r = db.records

# CHECK: Allow access to record without a password or not?
def get_record(record_id, password):
    return r.find_one({'_id': ObjectId(record_id), 'password': password})

def add_record(survey_submitted):
    added = r.insert_one(survey_submitted)
    record_id = added.inserted_id
    print('record ID: ' + record_id + ' added')
    return record_id
