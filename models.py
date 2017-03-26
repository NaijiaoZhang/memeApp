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

class potentialpartner(db.Model):
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
