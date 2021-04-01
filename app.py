from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.Routes import initialize_routes

app = Flask(__name__)
api = Api(app)


app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://admin:admin@cluster0.igcnz.mongodb.net/recommendDB?retryWrites=true&w=majority'
}

initialize_db(app)
initialize_routes(api)


if __name__ == "__main__":
    app.run()
