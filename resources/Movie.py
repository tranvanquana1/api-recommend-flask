from flask import Response, request, jsonify
from database.models import Movies
from flask_restful import Resource, reqparse


parser = reqparse.RequestParser()

parser.add_argument('page_index', type=int,
                    help='TYPE MUST INTEGER', default=1)
parser.add_argument('page_size', type=int,
                    help='TYPE MUST INTEGER', default=10)
parser.add_argument('keyword', type=str,
                    help='TYPE MUST STRING', default=None)


class MoviesResource(Resource):
    def get(self):
        args = parser.parse_args()
        page_index = args['page_index']
        page_size = args['page_size']
        keyword = args['keyword']

        movies = Movies.objects(title__contains=keyword).paginate(
            page=page_index, per_page=page_size)

        return jsonify({
            "message": "Danh sach phim",
            "data": movies.items,
            "meta": {
                "page_index": page_index,
                "page_size": page_size,
                "total_page": movies.pages,
                "total_record": movies.total
            }
        })


#
parser.add_argument('movie_id', type=int,
                    help='TYPE MUST INTEGER')
parser.add_argument('title', type=str,
                    help='TYPE MUST STRING')
parser.add_argument('release_date', type=str,
                    help='TYPE MUST STRING')
parser.add_argument('video_release_date', type=str,
                    help='TYPE MUST STRING', default=None)
parser.add_argument('IMDb_URL', type=str,
                    help='TYPE MUST STRING')
parser.add_argument('category', default=None)
parser.add_argument('category_code', default=[
                    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


class MovieResource(Resource):
    def get(self):
        args = parser.parse_args()
        movie_id = args['movie_id']

        if not movie_id:
            return jsonify({
                "message": "Thieu tham so movie_id",
                "data": None
            })

        movie = Movies.objects(movie_id=movie_id).first()

        if not movie:
            return jsonify({
                "message": "Phim khong ton tai",
                "data": None
            })

        return jsonify({
            "message": "Chi tiet phim",
            "data": movie
        })

    def post(self):
        args = parser.parse_args()

        title = args['title']
        release_date = args['release_date']
        video_release_date = args['video_release_date']
        IMDb_URL = args['IMDb_URL']
        category = args['category']
        category_code = args['category_code']

        if not title:
            return jsonify({
                "message": "thieu tham so title",
                "data": None
            })
        if not release_date:
            return jsonify({
                "message": "thieu tham so release_date",
                "data": None
            })
        if not IMDb_URL:
            return jsonify({
                "message": "thieu tham so title",
                "data": None
            })

        movie_id = Movies.objects().count() + 1
        print(movie_id)

        movie = Movies(movie_id=movie_id, title=title, release_date=release_date,
                       video_release_date=video_release_date, IMDb_URL=IMDb_URL, category=category, category_code=category_code)

        return jsonify({
            "message": 'them moi thanh cong',
            "data": movie
        })
