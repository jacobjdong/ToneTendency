# app.py

# Required imports
import time
import joblib
import numpy as np
import joblib as joblib
import librosa
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
audio_sentiment_map = ['angry', 'calm', 'digust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

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
    data = str(request.)
    print("hey")

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
    x_pred = AudioModel.predict_proba(x_pred)
    final_pred = encoder.inverse_transform(x_pred)
    return final_pred[0,0]


app.run(threaded=True, host='localhost', port=8081)