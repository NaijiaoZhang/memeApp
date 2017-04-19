from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import os
from ranked import RBO, getRankedList, convertToDict

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
current = 1

@app.route('/discover')
def discover_page():
    memes = db.session.query(models.Meme).all()
    return render_template('meme-pg.html',memes=memes)

@app.route('/results/<userId>')
def match_results(userId):
    currentUser = db.session.query(models.tagcount).filter_by(uid=userId)
    partners = db.session.query(models.tagcount).filter(models.tagcount.uid != userId).all()
    
    print "look here"
    print currentUser[0].uid
    print "fuck"
    
    myDict = convertToDict(currentUser[0])
    myTagList = getRankedList(myDict)
    
    potentialPartners = {}
    for p in partners:
        partnerDict = convertToDict(p)
        pList = getRankedList(partnerDict)
        potentialPartners[p.uid] = RBO(myTagList, pList)
        
    finalPartners = getRankedList(potentialPartners)    
    
    # return render_template('match-results-pg.html', partners=partners)
    return render_template('match-results-pg.html', partners=finalPartners)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        users = db.session.query(models.Users).filter_by(name=request.form['username'])
        particularUser = users[0]
        session['name']=particularUser.name
        password = users[0].password
        if request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in']=True
            return redirect(url_for('profile_page',userId=particularUser.uid))
    return render_template('layout.html', error=error)

@app.route('/profile/<userId>')
def profile_page(userId):     
    users = db.session.query(models.tagcount).filter_by(uid=userId) 
    # tagcount
    name = db.session.query(models.Users).filter_by(uid=userId)
    # user
    particularUser = users[0]
    particularName = name[0]
    return render_template('profile-pg.html',particularUser=particularUser,particularName=particularName)

@app.route('/memes', methods = ['GET', 'POST'])
def landing_page(): 
    
    global current 
    meme = db.session.query(models.Meme).filter(models.Meme.memeid == current).one() 
    
    if request.method == 'POST':
        #if request.form['submit'] == 'NO':
        '''opinion = models.Opinion(2, 4, 1)
         
        db.session.add(opinion)
        db.session.commit()
        flash('-Record was successfully added')

        meme = db.session.query(models.Meme).filter(models.Meme.memeid == 3).one()'''
            
        if request.form['submit'] == 'YES':
            opinion = models.Opinion(8, current, 1)
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')
            current += 1
            meme = db.session.query(models.Meme).filter(models.Meme.memeid == current).one()
            
            
        elif request.form['submit'] == 'NO':
            opinion = models.Opinion(8, current, 0)
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')
            
            current += 1
            meme = db.session.query(models.Meme).filter(models.Meme.memeid == current).one()   
    
    return render_template('meme-pg-new.html', meme = meme)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
