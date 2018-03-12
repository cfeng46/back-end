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
o = db.organizations

def get_organization(id):
    if id is None:
        return o.find()
    else:
        return o.find({'_id': id})

def get_organizations_by_tags(tags=List[int]):
    result_with_dupes = []
    for tag in tags:
        result_with_dupes.append(o.find({tags: tag}))
    result_cleaned = result_with_dupes[0]
    for i in range(1, len(result_with_dupes)):
        result_cleaned =  list(set(result_cleaned + i))
    return result


#LATER: sort or trim organizations by proximity
