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
records = db.records



# return full list of questions
# pulls all question documents from the question collection
def get_questions():
    questions_list = questions.find()
    print(questions_list)
    return questions_list

# insert document from completed survey to record collection
# takes location and list of tags POSTed
def insert_record(location, populations, services, languages):
    record = {
       'location': location,
       'populations': populations,
       'services': services,
       'languages': languages,
       'password': ''
    }
    print(records.count())
    records.insert_one(record)


# return organization based on given id
def get_org_by_ID(id):
    return json_util.dumps(organizations.find_one({'_id': ObjectId(id)}), default=json_util.default)

def get_orgs():
    return json_util.dumps(organizations.find(), default=json_util.default)


# return all organizations that match mandatory demographic tags
def find_orgs_by_matching_tags(survey_id):
    survey = records.find_one({'_id': ObjectId(survey_id)})
    organization_list = []
    for org in organizations.find({'populations': {'$exists': True}}):
        valid = True
        for item in survey['populations']:
            if item not in org['populations'] or survey['languages'] not in org['languages']:
                valid = False
                break
        if valid:
            organization_list.append(org)
            # print(org["populations"])
            # print(org['languages'])

    return organization_list
    ''' orgsList = []
    for category in surv:
        for value in category:
            item = db.organizations.find({category: value})
            print(item.explain())
            if(item.count()>0):
                item_json = json_util.dumps(list(item), default=json_util.default)
                orgsList.append(item_json)
    print(orgsList)'''


# gets organizations based on location of survey
def get_orgs_near_location(orgs, survey_id):
    survey = records.find_one({'_id': ObjectId(survey_id)})
    geolocator = Nominatim()
    location = geolocator.geocode(survey['location'])
    local_orgs = []
    for org in orgs:
       # coord = org['coordinates']
        print(org['coordinates']['latitude'])
        org_loc = org['coordinates']['latitude'], ', ', org['coordinates']['longitude']
        print(org_loc)
        survey_loc = str(location.latitude) + ', ' + str(location.longitude)
        distance = vincenty(survey_loc, org_loc).miles
        print(distance)
        if distance <= 50:
            local_orgs.append(org)
            print(org['coordinates'])
    return local_orgs


# returns organizations from the list of mandatory
# that include at least one service that they need
# takes the list of organizations and survey id to compare as parameters
def find_orgs_with_one_service(orgs, survey_id):
    survey = records.find_one({'_id': ObjectId(survey_id)})
    orgs_with_services = []
    for org in orgs:
        for service in survey['services']:
            if service in org['services']:
                if org in orgs_with_services:
                    break
                orgs_with_services.append(org)
            #print(service)
    return orgs_with_services


# updates user to include password
def update_password_by_id(survey_id, new_password):
    return records.find_one_and_update({'_id': survey_id}, {"$set": {'password': new_password}}, upsert=True)


# gets the users password from a survey record
def get_survey_password(survey_id):
    return records.find_one({'_id': ObjectId(survey_id)})
