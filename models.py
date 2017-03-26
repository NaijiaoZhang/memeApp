from sqlalchemy import sql, orm
from app import db


class Meme(db.Model):
    _tablename_ = 'meme'
    memeid = db.Column('memeid', db.Integer(), primary_key=True)
    caption = db.Column('caption', db.String(256))
    filepath = db.Column('filepath',db.String(256))
    imagename = db.Column('imagename',db.String(256))

class PotentialPartner(db.Model):
    _tablename_ = 'potential_partner'
    uid = db.Column('uid', db.Integer(), primary_key=True)
    partner = db.Column('partner', db.Integer(), primary_key=True)

class Users(db.Model):
    _tablename_ = 'users'
    name = db.Column('name', db.Integer(), primary_key=True)
    password = db.Column('password', db.String(256))
    avatar = db.Column('avatar', db.String(256))
