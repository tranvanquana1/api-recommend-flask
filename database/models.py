from .db import db
import datetime


class Categories(db.Document):
    title = db.StringField(required="ERROR_TITLE_MISSING", unique=True)
    IMDb_URL = db.ListField(db.StringField(), required=True)
    status = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    update_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Movies(db.Document):
    title = db.StringField(required="ERROR_TITLE_MISSING", unique=True)
    IMDb_URL = db.ListField(db.StringField(), required=True)
    release_date = db.ListField(db.StringField(), required=True)
    video_release_date = db.StringField(default=None)
    category = db.ListField(db.ReferenceField(Categories))
    status = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    update_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Users(db.Document):
    username = db.StringField(required="ERROR_NAME_MISSING", unique=True)
    password = db.StringField(required="ERROR_PASSWORD_MISSING")
    fullname = db.StringField(default=None)
    mobile = db.StringField(default=None)
    status = db.IntField(default=0)
    token = db.StringField(default=None)
    movies = db.ListField(db.DictField())
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    update_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Ratings(db.Document):
    all_rating = db.StringField(required="ERROR_NAME_MISSING")
