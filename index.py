from flask import Flask, render_template, request, json, redirect, jsonify
from flask_pymongo import pymongo
from flask_cors import CORS
from bson import json_util
import os
import bcrypt
import database.queries as queries
import database.survey as survey
import database.record as record

app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb://admin:intercept@45.55.198.145/interceptDB")
db = client.interceptDB

# Survey related
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    # return a list of questions for a new survey
    if request.method == 'GET':
        category_id = request.args.get('categoryId')
        print('tagID selected: ' + category_id)
        return jsonify(survey.get_questions(category_id))
    # LATER: TBA
    if request.method == 'POST':
        return 'TBA'


# Record related
@app.route('/record', methods=['GET', 'POST'])
def record():
    # return a record without password (currently not in use)
    if request.method == 'GET':
        record_id = request.args.get('recordId')
        print('getting record ID: ' + record_id)
        return jsonify(record.get_record(record_id))
    # survey submitted by user
    elif request.method == 'POST':
        # LATER: additional password option
        # First, add a record, which contains question-answer combination and relevant tag IDs
        record_id = record.add_record(request.get_json())
        record = record.get_record(record_id)
        print('returning search result using recordID: ' + record_id)
        # Return a list of organization based on tags from newly added record
        return jsonify(organization.get_organizations_by_tags(record['tags']))

# Record with password protection (Note the URL fragment for record ID)
@app.route('/record/<int:record_id>', methods=['POST'])
def protected_record():
    password = request.form['password']
    return record.get_protected_record(record_id, password)

# Organization related
@app.route('/organization', methods=['GET'])
def organization():
    return jsonify(o.get_organization(request.args.get('id')))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5050"))
    app.run(debug=True)
