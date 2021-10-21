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

    cursor.execute(
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    )
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
    game_id = request.form['game-id']
    game_score = request.form['score']
    param_value = request.form['param-id']
    
    conn = connect()
    cursor = conn.cursor()
    # TODO: write score to database
    cursor.execute(
        """
    
        """
    )
    conn.close()


    toReturn = """{
        "status": "success",
        "message": ""
    }"""
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
            "user_id": i[4],
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
    query = """
        SELECT * FROM games
        WHERE game_id = {0}
    """
    cursor.execute(query.format(game_id))

    results = []
    for i in cursor:
        results.append({
            "game_id": i[0],
            "name": i[1],
            "publisher": i[2],
            "description": i[3],
            "user_id": i[4],
        })

    toReturn = {
        "data": results
    }

    conn.close()
    
    return toReturn


# - example: http://127.0.0.1:5000/game-scores?game_id=1&param_id=1
@app.route('/game-scores', methods=['GET'])
def get_game_scores():
    game_id = request.args.get('game_id')
    param_id = request.args.get('game_id')
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
