from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.Routes import initialize_routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    # for user in rd.users.values:

    #     u = models.Users(user_id=user[0], username=str(user[0]), password=str(user[0]),
    #                      age=user[1], sex=user[2], occupation=user[3], zip_code=user[4])
    #     u.save()
    # print(u.user_id, u.username,
    #       u.password, u.age, u.sex, u.occupation, u.zip_code)

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
