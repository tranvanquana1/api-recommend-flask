from flask import Response, request
from flask_restful import Resource
from content_base_filter import precision
import json


class PredictResource(Resource):
    def get(self):

        user_id = request.args.get('user_id')

        if not user_id:
            return {
                "message": "thieu tham so user_id",
                "data": None
            }

        if user_id:
            id = int(user_id)
            return {
                "message": "Recommend movie",
                "data": json.loads(precision(id))
            }
