# app.py

# Required imports
import time
import joblib
import numpy as np
import joblib
import librosa
from numpy.lib.function_base import extract
import tensorflow

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow import keras
from flask import Flask, request
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer

# Initialize Flask app
app = Flask(__name__)
Sentences= {}

AudioModel = keras.models.load_model("./data/audioclassifier/audiomodel")
encoder = joblib.load("./data/audioclassifier/encoder.save") 
scaler = joblib.load("./data/audioclassifier/scaler.save") 
workdir = "./data/working/"
audio_predict_order = ['Anger', 'Calm', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']

Emotions = ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]
TextModel = joblib.load('./data/textclassifier/classifier.joblib.pkl')
TextModelVectorizer = joblib.load('./data/textclassifier/vectorizer.joblib.pkl')

@app.route('/addWord', methods=['POST'])
def create():
    # Ryan code here
    returnBody = ""
    data = str(request.get_data(as_text=True))
    sentence = data.split(",")
    id = str(sentence[0])

    if id not in Sentences:
        now = int(time.time())
        Sentences[str(now)] = ""
        return str(now)
    
    
    Sentences[id] = Sentences[id] + " " + str(sentence[1])
    matrix = TextModelVectorizer.transform([Sentences[sentence[0]]])
    predictions = TextModel.predict_proba(matrix)
    predictions = predictions[0].tolist()
    sum = 0.0
    for i in range(1, len(predictions)):
        sum = sum + predictions[i]
    factor = 1 / sum 
    for i in range(1, len(predictions)):
        returnBody = returnBody + Emotions[i] + ":"
        returnBody = returnBody + str(predictions[i] * factor) + ","
    
    return returnBody[:-1]



@app.route('/endSentence', methods=['POST'])
def read():
    file = request.form['file']
    data = request.form['id']
    matrix = TextModelVectorizer.transform([Sentences[data]])
    predictions = TextModel.predict_proba(matrix)
    predictions = predictions[0].tolist()
    file1 = open("temp.wav", "w")
    file1.write(str(file))
    voicePredictions = predict("temp.wav")

    for i in range(1, len(predictions)):
        sum = sum + predictions[i]
    factor = 1 / sum 

    returnBody = "Anger: " + ((voicePredictions["Anger"] + (predictions[1] * factor)) / 2)
    returnBody = returnBody + "Disgust: " + ((voicePredictions["Disgust"] + (predictions[2] * factor)) / 2)
    returnBody = returnBody + "Fear: " + ((voicePredictions["Fear"] + (predictions[3] * factor)) / 2)
    returnBody = returnBody + "Happiness: " + ((voicePredictions["Happiness"] + (predictions[4] * factor)) / 2)
    returnBody = returnBody + "Sadness: " + ((voicePredictions["Sadness"] + (predictions[5] * factor)) / 2)
    returnBody = returnBody + "Surprise: " + ((voicePredictions["Surprise"] + (predictions[6] * factor)) / 2)

def extract_features(data, sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result=np.hstack((result, zcr)) # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft)) # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc)) # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms)) # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel)) # stacking horizontally
    
    return result

def predict(path) :
    data, sample_rate = librosa.load(path)
    data, _ = librosa.effects.trim(data, top_db=20, frame_length=256, hop_length=64)
    X = []
    X.append(np.array(extract_features(data, sample_rate)))
    X = scaler.transform(X)
    x_pred = np.expand_dims(X, axis=2)
    x_pred = AudioModel.predict(x_pred)
    result = {}
    result[audio_predict_order[0]]= x_pred[0,0]
    for x in range(2, 8):
        result[audio_predict_order[x]]= x_pred[0,x]
    return result


app.run(threaded=True, host='localhost', port=8081)