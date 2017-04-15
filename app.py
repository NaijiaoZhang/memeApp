from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import models
import forms
import os

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

'''
@app.route('/')
def landing_page():
<<<<<<< HEAD
    return render_template('layout.html')
=======
    memes = db.session.query(models.Meme).all()
    return render_template('meme-pg-new.html',memes=memes)'''
>>>>>>> 250226ec97a37054e0d6214e090c8a3c4d1e1ce7

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
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

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

'''
@app.route('/drinker/<name>')
def drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    return render_template('drinker.html', drinker=drinker)

@app.route('/edit-drinker/<name>', methods=['GET', 'POST'])
def edit_drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    beers = db.session.query(models.Beer).all()
    bars = db.session.query(models.Bar).all()
    form = forms.DrinkerEditFormFactory.form(drinker, beers, bars)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.edit(name, form.name.data, form.address.data,
                                form.get_beers_liked(), form.get_bars_frequented())
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-drinker.html', drinker=drinker, form=form)
    else:
        return render_template('edit-drinker.html', drinker=drinker, form=form)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural
'''
if __name__ == '__main__':
<<<<<<< HEAD
=======

    print "HIHIHI"
>>>>>>> 250226ec97a37054e0d6214e090c8a3c4d1e1ce7
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
