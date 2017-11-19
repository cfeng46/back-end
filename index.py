from flask import Flask, render_template, request, json, redirect, jsonify, session
from flask_pymongo import pymongo
from bson import json_util
import database.queries as queries
import os

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:intercept@45.55.198.145/interceptDB")
db = client.interceptDB


@app.route('/testSurvey')
def surveyMatch():
    surveyID = request.args.get('id', default='*', type=str)

    return queries.find_orgs_by_matching_tags(surveyID)

'''Load questions for /questions GET'''
@app.route('/questions')
def questions():
    data = queries.get_questions()
    return data


@app.route('/organization')
def organization():
    org_ID = request.args.get('id', default=None, type=str)
    if(org_ID == None):
        orgs = queries.get_orgs()
    else:
        orgs = queries.get_org_by_ID(org_ID)
    return orgs



'''We receive a JSON for this POST, so we handle it accordingly using Flask's JSON functionality'''


@app.route('/survey_submit', methods=['POST'])
def save_survey():
    json_Dictionary = request.get_json()
    '''do stuff with jsonDict- parse into format for DB insert'''
    print("test survey submit")


if __name__ == '__main__':
    app.run()
