from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from random import randint
import models
import forms
import os
from ranked import RBO, getRankedList, convertToDict

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
current = 1
tagMeme = 1;


@app.route('/logout')
def logout(): 
    session['logged_in']=False
    return redirect(url_for('login'))

@app.route('/display')
def discover_page():
    memes = db.session.query(models.Meme).all()
    return render_template('meme-pg.html',memes=memes)

@app.route('/results/<userId>')
def match_results(userId):
    currentUser = db.session.query(models.tagcount).filter_by(uid=userId)
    nameList=None
    if(currentUser.count()!=0):
        partners = db.session.query(models.tagcount).filter(models.tagcount.uid != userId).all()
        myDict = convertToDict(currentUser[0])
        myTagList = getRankedList(myDict)
           
        potentialPartners = {}
        for p in partners:
            partnerDict = convertToDict(p)
            pList = getRankedList(partnerDict)
            potentialPartners[p.uid] = RBO(myTagList, pList)
                
        finalPartners = getRankedList(potentialPartners)
        nameList = []
        for partner in finalPartners: 
            user = db.session.query(models.Users).filter_by(uid=partner).one() 
            name = user.name
            nameList.append(name)

    # return render_template('match-results-pg.html', partners=partners)
    return render_template('match-results-pg.html', partners=nameList, userId=userId)

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

    numMemes = db.session.query(db.func.max(models.Meme.memeid)).scalar()
    memeIDOne = randint(1,numMemes)
    memeIDTwo = randint(1,numMemes)
    memeIDThree = randint(1,numMemes)
    memePicOne = db.session.query(models.Meme).filter_by(memeid=memeIDOne).one()
    memePicTwo = db.session.query(models.Meme).filter_by(memeid=memeIDTwo).one()
    memePicThree = db.session.query(models.Meme).filter_by(memeid=memeIDThree).one()
    # user
    particularUser = None
    if(users.count()!=0):
        particularUser = users[0]
    particularName = name[0]
    return render_template('profile-pg.html',particularUser=particularUser,particularName=particularName,userId=userId,
        picOne=memePicOne.filepath,picTwo=memePicTwo.filepath,picThree=memePicThree.filepath)

@app.route('/memes/<userId>', methods = ['GET', 'POST'])
def landing_page(userId): 
    global current
    global numMemes
    numMemes = db.session.query(db.func.max(models.Meme.memeid)).scalar()
    randomMeme = randint(1,numMemes)
    current = randomMeme
    meme = db.session.query(models.Meme).filter(models.Meme.memeid == current).one() 

    if request.method == 'POST':            
        if request.form['submit'] == 'YES':
            opinion = models.Opinion(userId, current, 1) 
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')

        elif request.form['submit'] == 'NO':
            opinion = models.Opinion(userId, current, 0) 
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')
            
    return render_template('meme-pg-new.html', meme=meme,userId=userId)



@app.route('/registration' , methods=['POST'])
def registration(): 
    if request.method == 'POST':
        loweredName = request.form['username'].lower()
        users = db.session.query(models.Users).filter_by(name=loweredName)
        largestUid = db.session.query(db.func.max(models.Users.uid)).scalar()
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
        
        
@app.route('/tags', methods = ['GET', 'POST'])
def assign_tags(): 
    global tagMeme
    meme = db.session.query(models.Meme).filter(models.Meme.memeid == tagMeme).one() 
    
    if request.method == 'POST':
        
        selected = request.form.getlist('tag')
        
        for i in selected:
            hastag = models.hastag(tagMeme, i)
            db.session.add(hastag)
            db.session.commit()
  
        tagMeme += 1
    
    return render_template('tag-pg.html', meme = meme)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
