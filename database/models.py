from .db import db
import datetime


class Categories(db.Document):
    category_id = db.IntField(required='ERROR_ID_MISSING', unique=True)
    title = db.StringField(required="ERROR_TITLE_MISSING", unique=True)
    status = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    update_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Movies(db.Document):
    movie_id = db.IntField(required='ERROR_ID_MISSING', unique=True)
    title = db.StringField(required="ERROR_TITLE_MISSING")
    release_date = db.StringField(required=True)
    video_release_date = db.StringField(default=None)
    IMDb_URL = db.StringField(required=True)
    category = db.ListField(db.ReferenceField(Categories))
    status = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    update_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Users(db.Document):
    user_id = db.IntField(required='ERROR_ID_MISSING', unique=True)
    username = db.StringField(required="ERROR_NAME_MISSING", unique=True)
    password = db.StringField(required="ERROR_PASSWORD_MISSING")
    fullname = db.StringField(default=None)
    age = db.IntField(default=None)
    sex = db.StringField(default=None)
    occupation = db.StringField(default="none")
    zip_code = db.StringField(default=None)
    status = db.IntField(default=0)
    token = db.StringField(default=None)
    movies = db.ListField(db.DictField())
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    update_at = db.DateTimeField(default=datetime.datetime.utcnow)
