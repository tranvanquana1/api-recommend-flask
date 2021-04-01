from flask import Response, request
from database.models import Users
from flask_restful import Resource
import json


class UserResource(Resource):
    def get(self):
        users = Users.objects().to_json()

        list_user = json.loads(users)
        return Response(users, mimetype="application/json", status=200)
