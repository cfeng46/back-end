import pymongo
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson import json_util
app = Flask(__name__)

# connect to the database
client = pymongo.MongoClient("mongodb://admin:intercept@45.55.198.145/interceptDB")
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
# takes location and list of tags POSTed
def insert_record(location, tags):
    record = {
       'location': location,
       'tags': tags,
       'password': ''
    }
    user = records.insert_one(record)
    print('One post: {0}'.format(insert_record(user)))


# return organization based on given id
def get_org_by_ID(id):
    return json_util.dumps(organizations.find_one({'_id': ObjectId(id)}), default=json_util.default)

def get_orgs():
    return json_util.dumps(organizations.find(), default=json_util.default)



def find_orgs_by_matching_tags(survey_id):
    survey = records.find_one({'_id': ObjectId(survey_id)})
    stuff = []
    for org in organizations.find({'populations':{'$exists':True}}):
        for tag in org["populations"]:
            for item in survey['populations']:
                if(tag==item):
                    stuff.append(org)
                    print(org["populations"])

    return stuff
    ''' orgsList = []
    for category in surv:
        for value in category:
            item = db.organizations.find({category: value})
            print(item.explain())
            if(item.count()>0):
                item_json = json_util.dumps(list(item), default=json_util.default)
                orgsList.append(item_json)
    print(orgsList)'''

# updates user with password
def update_password(survey_id, new_password):
    records.find_one_and_update({'ObjectId': survey_id}, {'password': new_password})


# returns list of applicable organizations
# based on the tags of the specific survey
#def find_organizations(survey_id):
#   survey = organizations.find({'id': survey_id})
 #  relevant_organizations = organizations.find([
  #     {'age': [survey['age'], {'gender': survey['gender']},
   #    {'special populations': survey['special populations']}
   #])

  # return relevant_organizations