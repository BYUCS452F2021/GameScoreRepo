import datetime
from flask import Flask, redirect, url_for, request, jsonify
from flask.json import JSONDecoder
from flask_cors import CORS
import json
import mysql.connector

app = Flask(__name__)
CORS(app)

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="myDB"
    )

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Game:
    def __init__(self, game_id, name):
        self.game_id = game_id
        self.name = name


def prepare_response(data):
    response = jsonify(data)
    return response


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


# - example: http://127.0.0.1:5000/login
#   should include parameters in form (form-data in postman)
@app.route('/login', methods=['POST'])
def login():
    form = json.loads(request.data.decode())
    username = form['username']
    password = form['password']

    conn = connect()
    cursor = conn.cursor()

    query = """
        SELECT * FROM users 
        WHERE username = %(username)s 
        AND password = %(password)s 
    """
    login_data = {
        'username': username, 
        'password': password
    }
    cursor.execute(query, login_data)
    rows = cursor.fetchall()
    conn.close()

    result = {}
    if len(rows) == 0:
        result = {
            "status": "fail",
            "message": "Unable to find user with specified username / password"
        }
    else:
        #TODO: this is a POST? should we record tokens or time of login?
        result = {
            "status": "success",
            "message": "",
            'username': rows[0][0],
            'email': rows[0][2]
        }
    return prepare_response(result)




# - example: http://127.0.0.1:5000/register
#   should include parameters in form (form-data in postman)
@app.route('/register', methods=['POST'])
def register():
    form = json.loads(request.data.decode())
    username = form['username']
    password = form['password']
    email = form['email']
    
    conn = connect()
    cursor = conn.cursor()

    # Verify that username does not already exist
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{username}'"
    )
    rows = cursor.fetchall()
    result = {}
    if len(rows) > 0:
        conn.close()
        result =  {
            "status": "fail", 
            "message": "User already exists"
        }
    else:
        query = "INSERT INTO users VALUES(%(username)s, %(password)s, %(email)s)"
        userData = {
            "username": username, 
            "password": password, 
            "email": email
        }
        cursor.execute(query, userData)
        conn.commit()
        conn.close()
        result =  {
            "status": "success", 
            "message": "",
            "username": username,
            "email": email
        }
    return prepare_response(result)


# - example: http://127.0.0.1:5000/score
#   should include parameters in form (form-data in postman)
@app.route('/score', methods=['POST'])
def score():
    form = json.loads(request.data.decode())
    game_id = form['game_id']
    value = form['value']
    username = form['username']
    
    conn = connect()
    cursor = conn.cursor()

    # check valid game
    cursor.execute(f"SELECT * FROM games WHERE game_id = {game_id} LIMIT 1")
    rows = cursor.fetchall()
    if len(rows) < 1:
        return prepare_response({
            "status": "fail",
            "message": "Invalid Game ID"
        })

    # check valid user
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1")
    rows = cursor.fetchall()
    if len(rows) < 1:
        return  prepare_response({
            "status": "fail",
            "message": "Invalid Username"
        })

    # insert new score
    query = (
        """
        INSERT INTO scores (game_id, value, username) 
        VALUES(%(game_id)s, %(value)s, %(username)s)
        """
    )
    score_data = {
        "game_id": game_id,
        "value": value,
        "username": username,
    }
    cursor.execute(query, score_data)
    conn.commit()
    conn.close()

    toReturn = {
        "status": "success",
        "message": ""
    }
    return prepare_response(toReturn)


# - example: http://127.0.0.1:5000/games
@app.route('/games', methods=['GET'])
def games():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM games
        """
    )

    results = []
    for i in cursor:
        results.append({
            "game_id": i[0],
            "name": i[1],
            "publisher": i[2],
            "description": i[3],
            "username": i[4],
        })

    conn.close()
    return prepare_response(results)


# - example: http://127.0.0.1:5000/game?game_id=1
@app.route('/game', methods=['GET'])
def game():
    game_id = request.args.get('game_id')
    
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM games WHERE game_id = {game_id}"
    cursor.execute(query)

    results = []
    for i in cursor:
        results.append({
            "game_id": i[0],
            "name": i[1],
            "publisher": i[2],
            "description": i[3],
            "username": i[4],
        })

    conn.close()
    
    return prepare_response(results)


# - example: http://127.0.0.1:5000/game_scores?game_id=1&param_id=1
@app.route('/game_scores', methods=['GET'])
def get_game_scores():
    game_id = request.args.get('game_id')
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM scores WHERE game_id = {game_id}")
    rows = cursor.fetchall()
    conn.close()

    return prepare_response(rows)

# - example: http://127.0.0.1:5000/user_scores?username=test
@app.route('/user_scores', methods=['GET'])
def get_user_scores():
    username = request.args.get('username')

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM scores WHERE username = '{username}'")
    rows = cursor.fetchall()
    conn.close()

    return prepare_response(rows)

# - example: http://127.0.0.1:5000/user?username=test
@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1")
    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 1:
        return prepare_response({
            "status": "fail",
            "message": "User not found"
        })

    return prepare_response({
        "status": "success",
        "username": rows[0][0],
        "email": rows[0][2],
    })

if __name__ == '__main__':
    app.run(debug=True)
