# app.py

# Required imports
import time
import joblib
import sys

from flask import Flask, request
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer

# Initialize Flask app
app = Flask(__name__)
Sentences= {}

Emotions = ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]
TextModel = joblib.load('./data/textclassifier/classifier.joblib.pkl')
TextModelVectorizer = joblib.load('./data/textclassifier/vectorizer.joblib.pkl')

@app.route('/addWord', methods=['POST'])
def create():
    # Ryan code here
    returnBody = ""
    data = str(request.get_data(as_text=True))
    sentence = data.split(",")

    if str(sentence[0]) not in Sentences:
        now = int(time.time())
        Sentences[str(now)] = ""
        return str(now)
    
    
    Sentences[sentence[0]] = Sentences[sentence[0]] + sentence[1]
    matrix = TextModelVectorizer.transform([Sentences[sentence[0]]])
    predictions = TextModel.predict_proba(matrix)
    predictions = predictions[0].tolist()
    for i in range(0, len(predictions)):
        returnBody = returnBody + Emotions[i] + ":"
        returnBody = returnBody + str(predictions[i]) + ","
    
    return returnBody[:-1]



@app.route('/endSentence', methods=['GET'])
def read():
    # Johnathan code here
    print("hey")


app.run(threaded=True, host='localhost', port=8081)