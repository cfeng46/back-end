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
    if request.method == 'GET':
        tag_id = request.args.get('tagId')
        print('tagID selected: ' + tag_id)
        return jsonify(survey.get_questions(tag_id))
    if request.method == 'POST':
        # LATER


# Record related
@app.route('/record', methods=['GET', 'POST'])
def record():
    if request.method == 'GET':
        record_id = request.args.get('recordId')
        print('getting record ID: ' + record_id)
        return jsonify(record.get_record(record_id))
    elif request.method == 'POST':
        # create a record and return search results
        # LATER: additional password option
        record_id = record.add_record(request.get_json())
        record = record.get_record(record_id)
        print('returning search result using recordID: ' + record_id)
        return jsonify(organization.get_organizations_by_tags(record['tags']))


# Organization related
@app.route('/organization', methods=['GET'])
def organization():
    return jsonify(o.get_organization(request.args.get('id')))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5050"))
    app.run(debug=True)
