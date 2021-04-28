from .Movie import MoviesResource, MovieResource
from .User import UserResource, LoginResource, UsersResource
from .Predict import PredictResource


def initialize_routes(api):
    api.add_resource(MovieResource, '/api/movie')
    api.add_resource(MoviesResource, '/api/list-movies')
    api.add_resource(PredictResource, '/api/predict')
    api.add_resource(UserResource, '/api/user')
    api.add_resource(UsersResource, '/api/list-user')
    api.add_resource(LoginResource, '/api/login')
