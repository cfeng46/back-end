from flask import Flask, render_template, request, redirect, jsonify, session
from flask_pymongo import PyMongo

app = Flask(__name__)

'''index- start==> InterceptDB query all questions'''

'''finish survey- POST back all tags-answers-->see what organizations satisfy their need'''



@app.route('/')
def hello_world():
    return "intercept hello"

@app.route('/login_submit', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']


if __name__ == '__main__':
    app.run()
