from .Movie import MoviesResource
from .User import UserResource
from .Predict import PredictResource


def initialize_routes(api):
    api.add_resource(MoviesResource, '/api/movies')
    api.add_resource(UserResource, '/api/user')
    api.add_resource(PredictResource, '/api/predict')
