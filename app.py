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

@app.route('/logout')
def logout(): 
    session['logged_in']=False
    return redirect(url_for('login'))

@app.route('/discover')
def discover_page():
    memes = db.session.query(models.Meme).all()
    return render_template('meme-pg.html',memes=memes)

@app.route('/results/<userId>')
def match_results(userId):
    currentUser = db.session.query(models.tagcount).filter_by(uid=userId)
    partners = db.session.query(models.tagcount).filter(models.tagcount.uid != userId).all()
    myDict = convertToDict(currentUser[0])
    myTagList = getRankedList(myDict)
    
    potentialPartners = {}
    for p in partners:
        partnerDict = convertToDict(p)
        pList = getRankedList(partnerDict)
        potentialPartners[p.uid] = RBO(myTagList, pList)
        
    finalPartners = getRankedList(potentialPartners)    
    
    # return render_template('match-results-pg.html', partners=partners)
    return render_template('match-results-pg.html', partners=finalPartners, userId=userId)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        loweredName = request.form['username'].lower()
        users = db.session.query(models.Users).filter_by(name=loweredName)
        if(users.count()!=0):
            particularUser = users[0]
            session['name']=particularUser.name
            password = users[0].password
            if request.form['password'] != password:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged_in']=True
                return redirect(url_for('profile_page',userId=particularUser.uid))
        else: 
            error = 'Invalid Crendentials. Please try again.'
    return render_template('layout.html', error=error)

@app.route('/<error>', methods=['GET', 'POST'])
def loginerror(error):
    if request.method == 'POST':
        loweredName = request.form['username'].lower()
        users = db.session.query(models.Users).filter_by(name=loweredName)
        if(users.count()!=0):
            particularUser = users[0]
            session['name']=particularUser.name
            password = users[0].password
            if request.form['password'] != password:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged_in']=True
                return redirect(url_for('profile_page',userId=particularUser.uid))
        else: 
            error = 'Invalid Crendentials. Please try again.'
    return render_template('layout.html', error=error)    

@app.route('/profile/<userId>')
def profile_page(userId):     
    users = db.session.query(models.tagcount).filter_by(uid=userId) 
    # tagcount
    name = db.session.query(models.Users).filter_by(uid=userId)
    # user
    particularUser = None
    if(users.count()!=0):
        particularUser = users[0]
    particularName = name[0]
    return render_template('profile-pg.html',particularUser=particularUser,particularName=particularName,userId=userId)

@app.route('/memes/<userId>', methods = ['GET', 'POST'])
def landing_page(userId): 
    
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
            opinion = models.Opinion(userId, current, 1) 
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')
            current += 1
            meme = db.session.query(models.Meme).filter(models.Meme.memeid == current).one()
            memeIndex = db.session.query(models.Meme).filter

        elif request.form['submit'] == 'NO':
            opinion = models.Opinion(userId, current, 0) 
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')
            current += 1
            meme = db.session.query(models.Meme).filter(models.Meme.memeid == current).one()   
    
    return render_template('meme-pg-new.html', meme=meme,userId=userId)

@app.route('/registration' , methods=['POST'])
def registration(): 
    if request.method == 'POST':
        loweredName = request.form['username'].lower()
        largestUid = db.session.query(db.func.max(models.Users.uid)).scalar()
        users = db.session.query(models.Users).filter_by(name=loweredName)
        if(users.count()==0):
            if(request.form['password']==request.form['confirm_password']):
                newUser = models.Users(largestUid+1,str(loweredName),str(request.form['password']),None,1)
                db.session.add(newUser)
                db.session.commit()
                flash('+Record was successfully added')
                return redirect(url_for('login'))
            else:
                error = 'Passwords do not match!'
                return redirect(url_for('loginerror', error=error))
        else: 
            error = 'User already exists!'
            return redirect(url_for('loginerror', error=error))

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
