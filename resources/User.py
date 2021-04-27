from flask import Response, request, jsonify
from database.models import Users
from flask_restful import Resource, reqparse
import json

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='TYPE MUST INTEGER')
parser.add_argument('username', type=str,
                    help='TYPE MUST STRING')
parser.add_argument('password', type=str,
                    help='TYPE MUST STRING')


class UserResource(Resource):
    def get(self):
        args = parser.parse_args()
        id = args['id']
        user = Users.objects(user_id=id)

        return jsonify({
            "message": "Danh sach user",
            "data": user,

        })

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

    def put(self):
        args = parser.parse_args()
        return jsonify({
            "message": 'thanh cong',
            "data": args
        })

    class ListUserResource(Resource):
        def get(self):
            users = Users.objects()

            return jsonify({
                "message": "Danh sach user",
                "data": users,
            })
