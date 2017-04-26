from sqlalchemy import sql, orm, ForeignKey
from app import db

class Users(db.Model):
    _tablename_ = 'users'
    uid = db.Column('uid', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(256))
    password = db.Column('password', db.String(256))
    facebookLink = db.Column('facebooklink', db.String(256), nullable=True)
    currentmeme = db.Column('currentmeme',db.Integer())

    def __init__(self,uid, name, password, facebookLink, currentmeme):
        self.uid = uid
        self.name = name
        self.password = password
        self.facebookLink = facebookLink
        self.currentmeme = currentmeme

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
    _tablename_ = 'isfriend'
    uid = db.Column('uid', db.Integer(), ForeignKey("Users.uid"), primary_key=True)
    friend = db.Column('friend', db.Integer(), ForeignKey("Users.uid"), primary_key=True)

class PotentialPartner(db.Model):
    _tablename_ = 'potentialpartner'
    uid = db.Column('uid', db.Integer(), ForeignKey("Users.uid"), primary_key=True)
    partner = db.Column('partner', db.Integer(), ForeignKey("Users.uid"), primary_key=True)

class Opinion(db.Model):
    _tablename_ = 'opinion'
    #uid = db.Column('uid', db.Integer(), ForeignKey("Users.uid"), primary_key=True)
    uid = db.Column('uid', db.Integer(), primary_key=True)
    #memeid = db.Column('memeid', db.Integer(), ForeignKey("Meme.memeid")) #buggy
    memeid = db.Column('memeid', db.Integer())
    preference = db.Column('preference', db.Integer())
    
    def __init__(self, uid=None, memeid=None, preference=None):
        self.uid = uid
        self.memeid = memeid
        self.preference = preference

class hastag(db.Model):
    _tablename_ = 'hastag'
    memeid = db.Column('memeid', db.Integer(), ForeignKey("meme.memeid"), primary_key=True)
    tagName = db.Column('tagname', db.String(256), ForeignKey("tag.name"), primary_key=True)
    
    def __init__(self, memeid, tagname):
        self.memeid = memeid
        self.tagName = tagname


# I HAVE NO IDEA WHY BUT SOME RELATIONS NEED TO BE ALL LOWER CASE?????
class tagcount(db.Model):
    _tablename_ = "TagCount"
    uid = db.Column('uid', db.Integer(), ForeignKey("users.uid"), primary_key=True)
    multipanel = db.Column('multipanel',db.Integer())
    celebrity = db.Column('celebrity',db.Integer())
    singleimage = db.Column('singleimage',db.Integer())
    anime = db.Column('anime',db.Integer())
    gaming = db.Column('gaming',db.Integer())
    politics = db.Column('politics',db.Integer())
    wholesome = db.Column('wholesome',db.Integer())
    race = db.Column('race',db.Integer())
    total = db.Column('total',db.Integer())

