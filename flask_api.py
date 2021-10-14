from flask import Flask, redirect, url_for, request
import jsons

app = Flask(__name__)


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Game:
    def __init__(self, game_id, name):
        self.game_id = game_id
        self.name = name


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


# - example: http://127.0.0.1:5000/login
#   should include parameters in form (form-data in postman)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # TODO: Return Actual User object
    user = User(username, password, 'garbage@gmail.com')
    return jsons.dump(user)


# - example: http://127.0.0.1:5000/register
#   should include parameters in form (form-data in postman)
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    # TODO: Verify that username does not already exist
    user = User(username, password, email)
    return jsons.dump(user)


# - example: http://127.0.0.1:5000/score
#   should include parameters in form (form-data in postman)
@app.route('/score', methods=['POST'])
def score():
    game_id = request.form['game-id']
    game_score = request.form['score']
    param_value = request.form['param-id']
    # TODO: write score to database
    toReturn = """{
    "status": "success",
    "message": ""
}"""
    return toReturn


# - examle: http://127.0.0.1:5000/games
@app.route('/games', methods=['GET'])
def games():
    # TODO: get list of games from database
    toReturn = """{
    "status": "success",
    "games": [
        {
            "game_id": 1,
            "name": "Catan"
        }
    ]
}"""
    return toReturn


# - example: http://127.0.0.1:5000/game?game-id=1
@app.route('/game', methods=['GET'])
def game():
    # TODO: get list game info form database
    game_id = request.args.get('game-id')
    toReturn = """{
    "status": "success"
    "game_id": "game_id_string",
    "name": "name_string",
    "publisher": "publisher_string",
    "description": "description_string",
    "username": "username_string",
    "params":[
        {
            "param_id": "game_id_string",
            "name": "game_name_string",
            "description": "param_description_string",
            "value": "param_value_string",
        },
        {
            "param_id": "game_id_string",
            "name": "game_name_string",
            "description": "param_description_string",
            "value": "param_value_string",
        },
    ],
}"""
    return toReturn


# - example: http://127.0.0.1:5000/game-scores?game-id=1&param-id=1
@app.route('/game-scores', methods=['GET'])
def get_game_scores():
    game_id = request.args.get('game-id')
    param_id = request.args.get('game-id')
    # TODO: get list of scores from database
    toReturn = """{
    "status": "success"
    "game_id": game_id_string,
    "param": {
        "param_id": game_id_string,
        "name": game_name_string,
        "description": param_description_string,
        "value": param_value_string,
    },
    "scores":[
        {
            "score_id": score_id_string,
            "value": value_number,
            "username": username_string,
            "date": date_string (Format: ISO 8601),
        },
        {
            "score_id": score_id_string,
            "value": value_number,
            "username": username_string,
            "date": date_string (Format: ISO 8601),
        },
    ],
}"""
    return toReturn


# - example: http://127.0.0.1:5000/user-scores?username=test
@app.route('/user-scores', methods=['GET'])
def get_user_scores():
    username = request.args.get('username')
    # TODO: get list of scores from database
    toReturn = """{
    "status": "success"
    "username": username_string,
    "scores":[
        {
            "score_id": score_id_string,
            "value": value_number,
            "date": date_string (Format: ISO 8601),
            "param_id": game_id_string,
            "param_name": param_name_string,
            "param_description": param_description_string,
            "param_value": param_value_string,
            "game_id": game_id_string,
            "game_name": game_name_string,
        },
        {
            "score_id": score_id_string,
            "value": value_number,
            "date": date_string (Format: ISO 8601),
            "param_id": game_id_string,
            "param_name": param_name_string,
            "param_description": param_description_string,
            "param_value": param_value_string,
            "game_id": game_id_string,
            "game_name": game_name_string,
        },
    ],
}"""
    return toReturn

# - example: http://127.0.0.1:5000/user?username=test
@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    # TODO: get user data from datbase
    user = User(username, "password", 'garbage@gmail.com')
    return jsons.dump(user)

if __name__ == '__main__':
    app.run(debug=True)
