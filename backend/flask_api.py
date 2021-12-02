import datetime
from flask import Flask, redirect, url_for, request, jsonify
from flask.json import JSONDecoder
from flask_cors import CORS
import json
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
CORS(app)

# Connect to DynamoDB tables
dynamo = boto3.resource('dynamodb')
user_table = dynamo.Table('users')
game_table = dynamo.Table('games')
score_table = dynamo.Table('scores')


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

    # In a real application we'd obviously salt and hash the password
    # and send it as part of our query, but this is easiest way for
    # a simple class project
    response = user_table.get_item(
        Key={
            'username': username
        }
    )

    item = response.get('Item')

    if item is None or item['password'] != password:
        result = {
            "status": "fail",
            "message": "Unable to find user with specified username / password"
        }
    else:
        #TODO: this is a POST? should we record tokens or time of login?
        result = {
            "status": "success",
            'username': item['username'],
            'email': item['email']
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

    # Verify that username does not already exist
    response = user_table.get_item(
        Key={
            'username': username
        }
    )

    result = {}
    if response.get('Item') is not None:
        result =  {
            "status": "fail", 
            "message": "User already exists"
        }
    else:        
        user_table.put_item(Item={
            "username": username, 
            "password": password, 
            "email": email
        })

        result =  {
            "status": "success", 
            "username": username,
            "email": email
        }
    return prepare_response(result)


# - example: http://127.0.0.1:5000/score
#   should include parameters in form (form-data in postman)
@app.route('/score', methods=['POST'])
def score():
    form = json.loads(request.data.decode())
    game = form['game']   # TODO: I changed this to game's name. The name of the game is a unique key and DynamoDB doesn't support auto-incremented primary keys
    value = form['value']
    username = form['username']
    # Not sure how this is coming in as data...
    # params = form['parameters']

    # check valid game
    response = game_table.get_item(
        Key={
            "name": game
        }
    )
    if response.get('Item') is None:
        return prepare_response({
            "status": "fail",
            "message": "Invalid Game"
        })
    
    # TODO: we should probably check that the given parameters
    # match the parameters in the game's attributes

    # check valid user
    response = user_table.get_item(
        Key={
            "username": username
        }
    )
    if response.get('Item') is None:
        return prepare_response({
            "status": "fail",
            "message": "Invalid Username"
        })

    # insert new score
    # DynamoDB doesn't support auto incrementing primary keys. So I've changed the scores table
    # to use a composite key, with game_name as the primary and a timestamp as the secondary.
    score_table.put_item(
        Item={
            "game": game,
            "timestamp": str(datetime.datetime.now()),
            "value": value,
            "username": username,
            # "parameters": params
        }
    )

    toReturn = {
        "status": "success"
    }
    return prepare_response(toReturn)


# - example: http://127.0.0.1:5000/game
#   should include parameters in form (form-data in postman)
@app.route('/game', methods=['POST'])
def add_game():
    form = json.loads(request.data.decode())
    name = form['name']
    publisher = form['publisher']
    description = form['description']
    username = form['username']
    # picture_file = form['picture']???

    # Make sure user is valid
    response = user_table.get_item(
        Key={
            "username": username
        }
    )
    if response.get('Item') is None:
        return prepare_response({
            "status": "fail",
            "message": "Invalid Username"
        })

    # TODO: add picture to an S3 bucket and get link to it

    game_table.put_item(
        Item={
            "name": name,
            "publisher": publisher,
            "description": description,
            "username": username
            # "image": s3_image_link
        }
    )

    return prepare_response({
        "status": "success"
    })


# - example: http://127.0.0.1:5000/games
@app.route('/games', methods=['GET'])
def games():
    response = game_table.scan()

    return prepare_response(response['Items'])


# - example: http://127.0.0.1:5000/game?name="Ticket to Ride"
@app.route('/game', methods=['GET'])
def game():
    name = request.args.get('name')

    response = game_table.get_item(
        Key={
            "name": name
        }
    )
    
    # TODO: return something useful when the item doesn't exist
    return prepare_response(response.get('Item'))


# - example: http://127.0.0.1:5000/game_scores?game_name=Ticket to Ride
@app.route('/game_scores', methods=['GET'])
def get_game_scores():
    game_name = request.args.get('game_name')
    
    response = score_table.query(
        KeyConditionExpression=Key('game').eq(game_name)
    )

    return prepare_response(response.get('Items'))

# - example: http://127.0.0.1:5000/user_scores?username=test
@app.route('/user_scores', methods=['GET'])
def get_user_scores():
    username = request.args.get('username')

    response = score_table.query(
        IndexName="username-index",
        KeyConditionExpression=Key('username').eq(username)
    )

    return prepare_response(response.get('Items'))

# - example: http://127.0.0.1:5000/user?username=test
@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    
    response = user_table.get_item(
        Key={
            "username": username
        }
    )

    if response.get('Item') is None:
        return prepare_response({
            "status": "fail",
            "message": "User not found"
        })

    return prepare_response({
        "status": "success",
        "username": response['Item']['username'],
        "email": response['Item']['email'],
    })

if __name__ == '__main__':
    app.run(debug=True)
