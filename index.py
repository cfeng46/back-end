from flask import Flask, render_template, request, json, redirect, jsonify, session
from flask_pymongo import pymongo
from bson import json_util
import database.queries as queries
import os
import bcrypt

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:intercept@45.55.198.145/interceptDB")
db = client.interceptDB

'''Load organizations that are relevant based on survey results'''
@app.route('/showSurveyResults')
def show_survey_results():
    surveyID = request.args.get('id', default='*', type=str)
    orgs = queries.find_orgs_by_matching_tags(surveyID)
    relevant_orgs = queries.find_orgs_with_one_service(orgs, surveyID)
    return json_util.dumps(relevant_orgs, default=json_util.default)

'''Updates the user password'''
@app.route('/password', methods=['POST'])
def create_password():
    surveyID = request.args.get('id', default='*', type=str)
    password = request.args.get('password', default='*', type=str)
    enc_pass = password.encode('utf-8')
    queries.update_password_by_id(surveyID, bcrypt.hashpw(enc_pass, bcrypt.gensalt(12)))
    return json_util.dumps(db.records.find(), default=json_util.default)

'''Checks the user password'''
@app.route('/login', methods=['POST'])
def login():
    surveyID = request.args.get('id', default='*', type=str)
    entered_password = request.args.get('password', default='*', type=str)
    survey_password = queries.get_survey_password(surveyID)
    if bcrypt.checkpw(entered_password, survey_password):
        surveyID = request.args.get('id', default='*', type=str)
        orgs = queries.find_orgs_by_matching_tags(surveyID)
        relevant_orgs = queries.find_orgs_with_one_service(orgs, surveyID)
        return json_util.dumps(relevant_orgs, default=json_util.default)
    else:
        return "No match"

'''Load questions for /questions GET'''
@app.route('/questions')
def questions():
    data = queries.get_questions()
    return data

'''Retrieves the provided organization if ID is present, or all
    orgs if the ID is nor present '''
@app.route('/organization')
def organization():
    org_ID = request.args.get('id', default=None, type=str)
    if(org_ID == None):
        orgs = queries.get_orgs()
    else:
        orgs = queries.get_org_by_ID(org_ID)
    return orgs

'''We receive a JSON for this POST, so we handle it accordingly using Flask's JSON functionality'''
@app.route('/surveySubmit', methods=['POST'])
def save_survey():
    json_Dictionary = request.get_json()
    '''do stuff with jsonDict- parse into format for DB insert'''
    print("test survey submit")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"))
