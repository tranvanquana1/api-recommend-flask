from flask import Response, request, jsonify
from database.models import Users
from flask_restful import Resource, reqparse
import json
from GoogleDriver import GoogleDriver

gd = GoogleDriver()

parser = reqparse.RequestParser()

parser.add_argument('username', type=str,
                    help='TYPE MUST STRING')
parser.add_argument('password', type=str,
                    help='TYPE MUST STRING')
# params method put
parser.add_argument('user_id', type=int, help='TYPE MUST INTEGER')
parser.add_argument('movie_id', type=int, help='TYPE MUST INTEGER')
parser.add_argument('rating', type=int, help='TYPE MUST INTEGER')


class UserResource(Resource):
    def get(self):
        args = parser.parse_args()
        user_id = args['user_id']
        user = Users.objects(user_id=user_id)

        if not user:
            return jsonify({
                "message": "user khong ton tai",
                "data": None
            })

        return jsonify({
            "message": "Danh sach user",
            "data": user,

        })

    def post(self):

        args = parser.parse_args()
        user_id = args['user_id']
        movie_id = args['movie_id']
        rating = args['rating']

        if not user_id:
            return jsonify({
                "message": "thieu tham so user_id",
                "data": None
            })
        if not movie_id:
            return jsonify({
                "message": "thieu tham so movie_id",
                "data": None
            })
        if not rating:
            return jsonify({
                "message": "thieu tham so rating",
                "data": None
            })

        gd.update_content(user_id, movie_id, rating)

        return jsonify({
            "message": 'thanh cong',
            "data": {
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating
            }
        })


# UsersResource params
parser.add_argument('page_index', type=int,
                    help='TYPE MUST INTEGER', default=1)
parser.add_argument('page_size', type=int,
                    help='TYPE MUST INTEGER', default=10)


class UsersResource(Resource):
    def get(self):
        args = parser.parse_args()
        page_index = args['page_index']
        page_size = args['page_size']

        users = Users.objects().paginate(page=page_index, per_page=page_size)

        if not users:
            return jsonify({
                "message": "Da co loi xay ra",
                "data": None
            })

        return jsonify({
            "message": 'Danh sach user',
            "data": users.items,
            "meta": {
                "page_index": users.page,
                "page_size": users.per_page,
                "total_page": users.pages,
                "total_record": users.total
            }
        })


class LoginResource(Resource):

    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        if not username:
            return {
                'message': 'username bat buoc nhap'
            }, 200

        if not password:
            return {
                'message': 'password bat buoc nhap'
            }, 200

        user = Users.objects(username=username).first()

        if user:
            if password == user.password:
                return jsonify({
                    "message": 'Dang nhap thanh cong',
                    "data": user
                })

            else:
                return {
                    "message": 'Mat khau khong chinh xac'
                }

        else:
            return {
                "message": 'Tai khoan khong chinh xac'
            }


class RegisterResource(Resource):

    def post(self):

        args = parser.parse_args()
        username = args['username']
        password = args['password']

        if not username:
            return jsonify({
                'message': 'username bat buoc nhap'
            })

        if not password:
            return jsonify({
                'message': 'password bat buoc nhap'
            })

        user = Users.objects(username=username).first()

        if not user:
            try:
                user_id = Users.objects().count() + 1
                new_user = Users(user_id=user_id, username=username,
                                 password=password)
                new_user.save()

                return jsonify({
                    "message": 'Tao tai khoan thanh cong',
                    "data": new_user
                })

            except Exception as e:
                print(e)
                return jsonify({
                    "message": 'Some error occurred. Please try again.',
                })

        else:
            return jsonify({
                "message": 'User already exists. Please Log in.'
            })
