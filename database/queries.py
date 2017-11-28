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
    return json_util.dumps(questions_list, default=json_util.default)

# insert document from completed survey to record collection
# takes location and a dictionary of tags


def insert_record(json_dict):
    # record = {
    #    'location': location,
    #    'populations': populations,
    #    'services': services,
    #    'languages': languages,
    #    'password': ''
    # }
    json_dict['password'] = ''
    print("length of dict inputted into db: ", len(json_dict))
    result = records.insert_one(json_dict)
    return result.inserted_id


# return organization based on given id
def get_org_by_ID(id):
    return json_util.dumps(organizations.find_one({'_id': ObjectId(id)}), default=json_util.default)

# return all organizations
def get_orgs():
    return json_util.dumps(organizations.find(), default=json_util.default)

# return organizations that are relevant given a dictionary of population, language, location, and service tags
# returns a list of relevant organizations
def get_relevant_orgs(front_end_json):
    survey_id = insert_record(front_end_json)
    print("This is survey_id: ", survey_id)
    base_orgs = find_orgs_by_matching_tags(survey_id)
    final_orgs = find_orgs_with_one_service(base_orgs, survey_id)
    final_orgs = get_orgs_near_location(final_orgs, survey_id)
    print("This is final orgs count: ", len(final_orgs))
    # for org in final_orgs:
    #     print(org)
    return json_util.dumps(final_orgs, default=json_util.default)

# return all organizations that match mandatory demographic tags
def find_orgs_by_matching_tags(survey_id):
    survey = records.find_one({'_id': ObjectId(survey_id)})
    organization_list = []
    for org in organizations.find({'populations': {'$exists': True}}):
        valid = True
        for item in survey['populations']:
            # if item not in org['populations'] or survey['languages'] not in org['languages']:
            if item not in org['populations']:
                valid = False
                break
        if valid:
            # print(org['name'])
            organization_list.append(org)
          
    return organization_list

# gets organizations based on location of survey
def get_orgs_near_location(orgs, survey_id):
    survey = records.find_one({'_id': ObjectId(survey_id)})
    print(survey.keys())
    print(survey['location'])
    geolocator = Nominatim()
    location = geolocator.geocode(survey['location'])
    local_orgs = []
    for org in orgs:
       # coord = org['coordinates']
       #  print(org['coordinates']['latitude'])
        # org_loc = org['coordinates']['latitude'], ', ', org['coordinates']['longitude']
        org_loc = (org['coordinates']['latitude'], org['coordinates']['longitude'])
        # print(org_loc)
        survey_loc = str(location.latitude) + ', ' + str(location.longitude)
        distance = vincenty(survey_loc, org_loc).miles
        # print(distance)
        if distance <= 100:
            local_orgs.append(org)
            print(org['name'])
            # print(org['coordinates'])
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
