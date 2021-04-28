from flask import Response, request, jsonify
from flask_restful import Resource, reqparse
from CF import CF
from GoogleDriver import GoogleDriver
from database.models import Movies, Users


#
gd = GoogleDriver()
rate_train = gd.rate_train
rate_train[:, :2] -= 1

rs = CF(rate_train, k=30, uuCF=0)

#
parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, help='TYPE MUST INTEGER')
parser.add_argument('page_size', type=int,
                    help='TYPE MUST INTEGER', default=10)


class PredictResource(Resource):
    def get(self):
        rs.fit()
        total_user = Users.objects().count()
        args = parser.parse_args()
        user_id = args['user_id']
        page_size = args['page_size']

        if user_id == None:
            return jsonify({
                "message": "thieu tham so user_id",
                "data": None
            })

        if user_id < 1 or user_id > total_user:
            return jsonify({
                "message": "user không tồn tại",
                "data": None
            })

        if user_id:
            array_movies_id = rs.recommend2(user_id-1, page_size)[:, 0]

            result = Movies.objects(
                movie_id__in=array_movies_id)

            return jsonify({
                "message": "Recommend movie",
                "data": result,
                "meta": {
                    "page_size": page_size,
                }
            })
