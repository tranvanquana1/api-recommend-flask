from flask import Response, request, jsonify
from flask_restful import Resource
from CF import CF
from GoogleDriver import GoogleDriver
from database.models import Movies

#
gd = GoogleDriver()
rate_train = gd.rate_train
rate_train[:, :2] -= 1

rs = CF(rate_train, k=30, uuCF=0)


class PredictResource(Resource):
    def get(self):
        rs.fit()
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({
                "message": "thieu tham so user_id",
                "data": None
            })

        if user_id:
            id = int(user_id)
            array_movies_id = rs.recommend2(id)[:, 0]
            result = Movies.objects(
                movie_id__in=array_movies_id)

            return jsonify({
                "message": "Recommend movie",
                "data": result,
                "meta": {
                    "total_record": len(array_movies_id)
                }
            })
