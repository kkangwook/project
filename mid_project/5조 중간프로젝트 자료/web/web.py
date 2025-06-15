from flask import Flask, render_template, redirect, request, session

app=Flask(__name__)

import numpy as np
import pickle
from xgboost import XGBClassifier

f=open('./rmodel.pickle','rb')
model=pickle.load(f)
f.close()

def camelot_sin(x):
    angle=2*np.pi*(x-1)/12
    return np.sin(angle)

def camelot_cos(x):
    angle=2*np.pi*(x-1)/12
    return np.cos(angle)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/result/', methods=['POST'])
def result():
    like=int(request.form['like'])
    bpm=int(request.form['bpm'])
    energy=int(request.form['energy'])
    danceability=int(request.form['danceability'])
    acousticness=int(request.form['acousticness'])
    camelot_number=int(request.form['camelot_number'])
    cs=camelot_sin(camelot_number)
    cc=camelot_cos(camelot_number)
    camelot_ab=request.form['camelot_AB']
    ab=0 if camelot_ab=='A' else 1
    genre=request.form['genre']
    if genre=='rbsoul':
        ohe=[0,0,0,0,0,0,0,0]
    elif genre=='기타':
        ohe=[1,0,0,0,0,0,0,0]
    elif genre=='댄스':
        ohe=[0,1,0,0,0,0,0,0]
    elif genre=='랩힙합':
        ohe=[0,0,1,0,0,0,0,0]
    elif genre=='록메탈':
        ohe=[0,0,0,1,0,0,0,0]
    elif genre=='발라드':
        ohe=[0,0,0,0,1,0,0,0]
    elif genre=='성인가요트로트':
        ohe=[0,0,0,0,0,1,0,0]
    elif genre=='인디음악':
        ohe=[0,0,0,0,0,0,1,0]
    elif genre=='포크블루스':
        ohe=[0,0,0,0,0,0,0,1]    
    data=[[like,bpm,energy,danceability,acousticness,cs,cc,ab]+ohe]
    prob=model.predict_proba(data)
    return render_template('result.html', like=like, bpm=bpm, energy=energy, danceability=danceability,
                           camelot_number=camelot_number, cs=cs, cc=cc, camelot_ab=camelot_ab,
                           ab=ab, genre=genre, data=data, prob=prob)

app.run(host='0.0.0.0', port=3179)