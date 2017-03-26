from sqlalchemy import sql, orm
from app import db

class Users(db.Model):
    _tablename_ = 'users'
    uid = db.Column('uid', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(256))
    password = db.Column('password', db.String(256))
    avatar = db.Column('avatar', db.String(256), nullable=True)

class Meme(db.Model):
    _tablename_ = 'meme'
    memeid = db.Column('memeid', db.Integer(), primary_key=True)
    caption = db.Column('caption', db.String(256))
    filepath = db.Column('filepath',db.String(256))
    imagename = db.Column('imagename',db.String(256))

class Tag(db.Model):
    _tablename_ = 'tag'
    name = db.Column('name', db.String(256), primary_key=True)

class IsFriend(db.Model):
    _tablename_ = 'isFriend'
    uid = db.Column('uid', db.Integer(), primary_key=True)
    friend = db.Column('friend', db.Integer(), primary_key=True)

class PotentialPartner(db.Model):
    _tablename_ = 'potentialPartner'
    uid = db.Column('uid', db.Integer(), primary_key=True)
    partner = db.Column('partner', db.Integer(),  primary_key=True)

class Opinion(db.Model):
    _tablename_ = 'opinion'
    uid = db.Column('uid', db.Integer(),primary_key=True)
    memeid = db.Column('memeid', db.Integer())
    preference = db.Column('preference', db.Integer())

class hasTag(db.Model):
    _tablename_ = 'hasTag'
    memeID = db.Column('memeid', db.Integer(), primary_key=True)
    tagName = db.Column('tagname', db.String(256), primary_key=True)

class Drinker(db.Model):
    __tablename__ = 'drinker'
    name = db.Column('name', db.String(20), primary_key=True)
    address = db.Column('address', db.String(20))
    likes = orm.relationship('Likes')
    frequents = orm.relationship('Frequents')
    @staticmethod
    def edit(old_name, name, address, beers_liked, bars_frequented):
        try:
            db.session.execute('DELETE FROM likes WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('DELETE FROM frequents WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('UPDATE drinker SET name = :name, address = :address'
                               ' WHERE name = :old_name',
                               dict(old_name=old_name, name=name, address=address))
            for beer in beers_liked:
                db.session.execute('INSERT INTO likes VALUES(:drinker, :beer)',
                                   dict(drinker=name, beer=beer))
            for bar, times_a_week in bars_frequented:
                db.session.execute('INSERT INTO frequents'
                                   ' VALUES(:drinker, :bar, :times_a_week)',
                                   dict(drinker=name, bar=bar,
                                        times_a_week=times_a_week))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    

