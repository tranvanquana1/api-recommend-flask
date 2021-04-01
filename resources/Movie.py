from flask import Response, request
from database.models import Movies
from flask_restful import Resource
import json


class MoviesResource(Resource):
    def get(self):
        movies = Movies.objects().to_json()

        list_movie = json.loads(movies)
        # for item in list_movie:
        #     print(item._id)
        print(list_movie)
        return Response(movies, mimetype="application/json", status=200)
