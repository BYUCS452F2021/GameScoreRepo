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
  param_id      INT           NOT NULL,
  name          VARCHAR(255)  NOT NULL,
  game_id       INT           NOT NULL,
  description   VARCHAR(255)  NOT NULL,
  value         INT           NOT NULL,
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

# TODO: @Ashton fill with dummy data
print("Filling with dummy data...")
cursor.execute("INSERT INTO users VALUES ('brody', 'password', 'brody@rasmus.sen')")
cursor.execute("INSERT INTO games (name, publisher, description, username) VALUES ('Catan', 'pub', 'get sheep', 'brody')")
# cursor.execute("INSERT INTO ... ")

conn.commit()
conn.close()

print("Database Successfully initialized!")
