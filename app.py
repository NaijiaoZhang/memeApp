from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import os

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})


@app.route('/discover')
def discover_page():
    memes = db.session.query(models.Meme).all()
    return render_template('meme-pg.html',memes=memes)

@app.route('/results')
def match_results():
    partners = db.session.query(models.potentialpartner).filter_by(uid=2).all()
    allusers = db.session.query(models.Users).all()
    return render_template('match-results-pg.html', partners=partners, allusers=allusers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('profile'))
    return render_template('layout.html', error=error)

@app.route('/profile')
def profile_page():     
    memes = db.session.query(models.Meme).all()
    return render_template('profile-pg.html',memes=memes)


@app.route('/', methods = ['GET', 'POST'])
def landing_page():
    
    meme = db.session.query(models.Meme).filter(models.Meme.memeid == 4).one()

    if request.method == 'POST':
        #if request.form['submit'] == 'NO':
        opinion = models.Opinion(2, 4, 1)
         
        db.session.add(opinion)
        db.session.commit()
        flash('-Record was successfully added')

        meme = db.session.query(models.Meme).filter(models.Meme.memeid == 3).one()
            
        '''elif request.form['submit'] == 'YES':
            opinion = opinion(0, 0, 1)
         
            db.session.add(opinion)
            db.session.commit()
            flash('+Record was successfully added')
            meme = db.session.query(models.Meme).filter(models.Meme.memeid == 2).one()'''
    return render_template('meme-pg-new.html', meme = meme)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
