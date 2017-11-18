import pymongo
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_pymongo import PyMongo

app = Flask(__name__)

# connect to the database
client = pymongo.MongoClient()
db = client.interceptDB
# create collection
organizations = db.organizations
questions = db.questions
records = db.records


# return full list of questions
# pulls all question documents from the question collection
def get_questions():
    questions_list = questions.find({})
    return questions_list


# insert document from completed survey to record collection
def insert_record(location, tags):
    record = {
        'location': location,
        'tags': tags,
        'password': ''
    }
    user = records.insert_one(record)
    print('One post: {0}'.format(insert_record.user))


# returns list of applicable organizations
# based on the tags of the specific survey
def find_organizations(survey_id):
    survey = organizations.find({'id': survey_id})
    relevant_orgs = organizations.find({""})
