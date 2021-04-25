from flask import Response, request
from flask_restful import Resource
from content_base_filter import precision
from CF import CF
import json
import read_data as rd


class PredictResource(Resource):
    def get(self):
        #
        rate_train = rd.rate_data
        rate_train[:, :2] -= 1

        rs = CF(rate_train, k=30, uuCF=0)
        rs.fit()

        user_id = request.args.get('user_id')

        if not user_id:
            return {
                "message": "thieu tham so user_id",
                "data": None
            }

        if user_id:
            id = int(user_id)
            print('user_id: ', id)
            return {
                "message": "Recommend movie",
                "data":  json.loads(rs.print_recommendation_for_user(id))
            }
