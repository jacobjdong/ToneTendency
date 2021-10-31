import numpy as np
import joblib as joblib
# librosa is a Python library for analyzing audio and music. It can be used to extract the data from the audio files we will see it later.
import librosa

from sklearn.preprocessing import StandardScaler, OneHotEncoder
import tensorflow
from tensorflow import keras

import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning) 

model = keras.models.load_model("C:/Users/Jonathan Munoz/Projects/ToneTendency/AudioAnalysis/mymodel")
encoder = joblib.load("C:/Users/Jonathan Munoz/Projects/ToneTendency/AudioAnalysis/encoder.save") 
scaler = joblib.load("C:/Users/Jonathan Munoz/Projects/ToneTendency/AudioAnalysis/scaler.save") 

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
    x_pred = model.predict_proba(x_pred)
    final_pred = encoder.inverse_transform(x_pred)
    return final_pred[0,0]

