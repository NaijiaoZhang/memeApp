from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import os

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

@app.route('/results')
def match_results():
    partners = db.session.query(models.potentialpartner).filter_by(uid=2).all()
    return render_template('match-results-pg.html', partners=partners)

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

@app.route('/registration' , methods=['POST'])
def registration(): 
    if request.method == 'POST':
        print request.form['username']
        print request.form['password']
        print request.form['confirm_password']
        loweredName = request.form['username'].lower()
        largestUid = db.session.query(db.func.max(models.Users.uid)).scalar()
        users = db.session.query(models.Users).filter_by(name=loweredName)
        print "IM THE USER COUNT: "+str(users.count())
        if(users.count()==0):
            if(request.form['password']==request.form['confirm_password']):
                print "testing: "+loweredName
                newUser = models.Users(largestUid+1,str(loweredName),str(request.form['password']),None,1)
                db.session.add(newUser)
                db.session.commit()
                flash('+Record was successfully added')


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
