from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.Routes import initialize_routes
from database.models import Movies

app = Flask(__name__)


@app.route('/')
def index():
    return {
        "message": 'server is running'
    }


api = Api(app)


app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://admin:admin@cluster0.igcnz.mongodb.net/recommendDB?retryWrites=true&w=majority'
}

initialize_db(app)
initialize_routes(api)


if __name__ == "__main__":
    app.run()
    movie = Movies(title='hello', IMDb_URL=['hello'], release_date=[
        'hello'], video_release_date='hello', category=['hello'], status=1)
    movie.save()
