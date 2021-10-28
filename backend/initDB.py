import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="myDB"
)

print("Connection Successful")

cursor = conn.cursor()

print("Dropping old tables...")
cursor.execute("CREATE DATABASE IF NOT EXISTS myDB")  # TODO: you'll have to manually create myDB the first time
cursor.execute("DROP TABLE IF EXISTS ScoreParams")
cursor.execute("DROP TABLE IF EXISTS Params")
cursor.execute("DROP TABLE IF EXISTS Scores")
cursor.execute("DROP TABLE IF EXISTS Games")
cursor.execute("DROP TABLE IF EXISTS Users")

print("Creating new tables...")
# USERS
cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS Users (
  username   VARCHAR(255)  NOT NULL,
  password   VARCHAR(255)  NOT NULL,
  email      VARCHAR(255)  NOT NULL,
  PRIMARY KEY (username)
  )
  """
  )

# GAMES
cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS Games (
  game_id      INT AUTO_INCREMENT  NOT NULL,
  name         VARCHAR(255)        NOT NULL,
  publisher    VARCHAR(255)        NOT NULL,
  description  VARCHAR(255)        NOT NULL,
  username     VARCHAR(255)        NOT NULL,
  PRIMARY KEY (game_id),
  FOREIGN KEY (username) REFERENCES Users(username)
  )
  """
  )

# SCORES
cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS Scores (
  score_id INT AUTO_INCREMENT  NOT NULL, 
  game_id  INT                 NOT NULL, 
  value    INT                 NOT NULL, 
  username VARCHAR(255)        NOT NULL,
  date     DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (score_id),
  FOREIGN KEY (game_id) REFERENCES Games(game_id),
  FOREIGN KEY (username) REFERENCES Users(username)
  )
  """
  )

# PARAMS
cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS Params (
  param_id      INT AUTO_INCREMENT  NOT NULL,
  name          VARCHAR(255)        NOT NULL,
  game_id       INT                 NOT NULL,
  description   VARCHAR(255)        NOT NULL,
  value         INT                 NOT NULL,
  PRIMARY KEY (param_id),
  FOREIGN KEY (game_id) REFERENCES Games(game_id)
  )
  """
  )

# SCOREPARAMS
cursor.execute(
  """
  CREATE TABLE IF NOT EXISTS ScoreParams (
  score_id INT NOT NULL,
  param_id INT NOT NULL,
  FOREIGN KEY (score_id) REFERENCES Scores(score_id),
  FOREIGN KEY (param_id) REFERENCES Params(param_id)
  )
  """)

# Fill with dummy data
print("Filling with dummy data...")
# Users
cursor.execute("INSERT INTO users VALUES ('brody', 'password', 'brody@rasmus.sen')")
cursor.execute("INSERT INTO users VALUES ('ashton', 'password1', 'ashto@hammo.com')")
cursor.execute("INSERT INTO users VALUES ('braydon', 'password2', 'braydon@hunt.com')")
cursor.execute("INSERT INTO users VALUES ('jared', 'password3', 'jared@jacob.com')")
cursor.execute("INSERT INTO users VALUES ('nate', 'password4', 'nate@fasta.bend')")
# Games
cursor.execute("INSERT INTO games (name, publisher, description, username) VALUES ('Catan', 'Kosmos', 'Settle a new land!', 'brody')")
cursor.execute("INSERT INTO games (name, publisher, description, username) VALUES ('Ticket to Ride', 'Days of Wonder', 'Build choo-choo trains!', 'ashton')")
cursor.execute("INSERT INTO games (name, publisher, description, username) VALUES ('Carcassonne', 'Rio Grande Games', 'Shape the medieval landscape of France.', 'braydon')")
cursor.execute("INSERT INTO games (name, publisher, description, username) VALUES ('Terraform Mars', 'FryxGames', 'Make Mars habitable!', 'jared')")
cursor.execute("INSERT INTO games (name, publisher, description, username) VALUES ('7 Wonders', 'Repos Production', 'Earn points by building stuff with cards.', 'nate')")
# Scores
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (1, 11, 'brody')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (1, 10, 'ashton')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (2, 190, 'jared')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (2, 210, 'nate')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (3, 303, 'nate')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (3, 295, 'brody')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (4, 132, 'nate')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (4, 112, 'braydon')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (5, 79, 'ashton')")
cursor.execute("INSERT INTO scores (game_id, value, username) VALUES (5, 76, 'jared')")
# Params
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 1, 'number of players', 4)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 1, 'number of rounds to finish', 20)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 1, 'number of players', 5)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 1, 'number of rounds to finish', 18)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 2, 'number of players', 4)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 2, 'number of rounds to finish', 20)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 2, 'number of players', 3)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 2, 'number of rounds to finish', 19)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 3, 'number of players', 2)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 3, 'number of rounds to finish', 36)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 3, 'number of players', 5)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 3, 'number of rounds to finish', 15)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 4, 'number of players', 1)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 4, 'number of rounds to finish', 50)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 4, 'number of players', 5)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('rounds', 4, 'number of rounds to finish', 75)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 5, 'number of players', 4)")
cursor.execute("INSERT INTO params (name, game_id, description, value) VALUES ('players', 5, 'number of players', 3)")
# ScoreParams
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (1, 1)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (1, 2)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (2, 3)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (2, 4)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (3, 5)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (3, 6)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (4, 7)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (4, 8)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (5, 9)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (5, 10)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (6, 11)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (6, 12)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (7, 13)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (7, 14)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (8, 15)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (8, 16)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (9, 17)")
cursor.execute("INSERT INTO ScoreParams (score_id, param_id) VALUES (10, 18)")

conn.commit()
conn.close()

print("Database Successfully initialized!")
