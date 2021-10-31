# app.py

# Required imports
import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)
Sentences= {}

@app.route('/addWord', methods=['POST'])
def create():
    # Ryan code here
    str(request.get_data)
    now = int(time.time())
    Sentences[now] = ""
    return now

@app.route('/endSentence', methods=['GET'])
def read():
    # Johnathan code here


app.run(threaded=True, host='0.0.0.0', port=8080)