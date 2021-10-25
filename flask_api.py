import datetime
from flask import Flask, redirect, url_for, request
import jsons
import mysql.connector

app = Flask(__name__)

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
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


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


# - example: http://127.0.0.1:5000/login
#   should include parameters in form (form-data in postman)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
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
    if len(rows) == 0:
        return {
            "status": "fail",
            "message": "Unable to find user with specified username / password"
        }
    else:
        #TODO: this is a POST? should we record tokens or time of login?
        return {
            "status": "success",
            "message": f"Welcome, {username}!"
        }


# - example: http://127.0.0.1:5000/register
#   should include parameters in form (form-data in postman)
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    conn = connect()
    cursor = conn.cursor()

    # Verify that username does not already exist
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{username}'"
    )
    rows = cursor.fetchall()
    if len(rows) > 0:
        conn.close()
        return {
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
        return {
            "status": "success", 
            "message": "User created successfully",
            "user": userData
        }


# - example: http://127.0.0.1:5000/score
#   should include parameters in form (form-data in postman)
@app.route('/score', methods=['POST'])
def score():
    game_id = request.form['game_id']
    value = request.form['value']
    username = request.form['username']
    
    conn = connect()
    cursor = conn.cursor()

    # check valid game
    cursor.execute(f"SELECT * FROM games WHERE game_id = {game_id} LIMIT 1")
    rows = cursor.fetchall()
    if len(rows) < 1:
        return {
            "status": "fail",
            "message": "Invalid Game ID"
        }

    # check valid user
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1")
    rows = cursor.fetchall()
    if len(rows) < 1:
        return {
            "status": "fail",
            "message": "Invalid Username"
        }

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
        "message": "New score successfully recorded!",
        "score": score_data,
    }
    return toReturn


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

    toReturn = {
        "data": results
    }

    conn.close()

    return toReturn


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

    toReturn = {
        "data": results
    }

    conn.close()
    
    return toReturn


# - example: http://127.0.0.1:5000/game_scores?game_id=1&param_id=1
@app.route('/game_scores', methods=['GET'])
def get_game_scores():
    game_id = request.args.get('game_id')
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM scores WHERE game_id = {game_id}")
    rows = cursor.fetchall()
    conn.close()

    return {
        "data": rows
    }


# - example: http://127.0.0.1:5000/user_scores?username=test
@app.route('/user_scores', methods=['GET'])
def get_user_scores():
    username = request.args.get('username')

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM scores WHERE username = '{username}'")
    rows = cursor.fetchall()
    conn.close()

    return {
        "data": rows
    }

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
        return {
            "status": "fail",
            "message": "User not found"
        }
    else:
        return {
            "status": "success",
            "user": rows[0],
        }

if __name__ == '__main__':
    app.run(debug=True)
