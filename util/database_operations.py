import sqlite3
import bcrypt
import os

db_path = os.path.join("databases", "voting.db")

# Initialize the database
def create_db():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	# Creates a new table named 'users' in the 'voting.db' database if it doesn't already exist.
	# The table stores user information including username, hashed password, and authorization level.	
	cursor.execute('''
    CREATE TABLE IF NOT EXISTS "users" (
	"userId"	INTEGER NOT NULL,
	"username"	TEXT,
	"password"	TEXT,
	"authorization"	TEXT,
	PRIMARY KEY("userId" AUTOINCREMENT))''')
    
	# Creates a new table named 'candidates' in the 'voting.db' database if it doesn't already exist.
    # The table stores candidate information including name and image path.
	cursor.execute('''CREATE TABLE IF NOT EXISTS "candidates" (
	"candidateId"	INTEGER NOT NULL,
	"name"	TEXT,
	"imagepath"	TEXT,
	PRIMARY KEY("candidateId" AUTOINCREMENT))''')
    
	# Creates a new table named 'votes' in the 'voting.db' database if it doesn't already exist.
    # The table stores vote information including user ID and candidate ID for tracking votes.
	cursor.execute('''CREATE TABLE IF NOT EXISTS "votes" (
	"voteId"	INTEGER NOT NULL,
	"userId"	INTEGER NOT NULL,
	"candidateId"	INTEGER NOT NULL,
	PRIMARY KEY("voteId" AUTOINCREMENT))''')
    
	conn.commit()
	conn.close

# Checks if a user exists in the database based on username
def check_if_user_exists(user_name: str):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute('SELECT * FROM users WHERE username = ?', (user_name,))
	rows = cursor.fetchall()

	conn.close
	return (len(rows) > 0)  # Returns True if user exists, False otherwise

# Adds a new user to the database
def add_user(user_name: str, password: str, authorization: str):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	# Hash the password for secure storage
	password_bytes = password.encode('utf-8')
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password_bytes, salt)

	cursor.execute('INSERT INTO users (username, password, authorization) VALUES (?,?,?)', (user_name, hashed_password, authorization,))
	conn.commit()
	conn.close

# Verifies user login credentials
def check_login(user_name: str, password: str):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute('SELECT * FROM users WHERE username = ?', (user_name,))
	rows = cursor.fetchall()

	conn.close

	if len(rows) > 0:
		# Check if the password matches the hashed password in the database
		password_bytes = password.encode('utf-8')
		if bcrypt.checkpw(password_bytes, rows[0][2]):
			return (str(user_name), str(rows[0][3])) # Return username and authorization level if successful
		else:
			return ["INCORRECT_PASS"] # Return message indicating incorrect password
	else:
		return ["NOT_EXIST"] # Return message indicating user not found
			
# Adds a new candidate to the database
def add_candidate(candidate_name: str, candidate_image_path: str):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute('INSERT INTO candidates (name, imagepath) VALUES (?,?)', (candidate_name, candidate_image_path,))
	
	conn.commit()
	conn.close
	
# Gets a dictionary of all candidates in the database, key is candidate name, value is image path
def get_candidates():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	candidates = {}
	cursor.execute('SELECT * FROM candidates')
	rows = cursor.fetchall()

	for row in rows:
		candidates.update({row[1]: row[2]})

	conn.close

	return candidates

# Removes candidates from the database. If clear_all is True, all candidates are removed.
# Otherwise, a specific candidate can be removed by providing their candidate ID
def remove_candidates(clear_all: bool, candidate_id: int = -1):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	if clear_all:
		cursor.execute('DELETE FROM candidates')
	elif candidate_id > -1:
		cursor.execute('DELETE FROM candidates WHERE candidateId = ?', (candidate_id,))

	conn.commit()
	conn.close

# Gets the number of votes a specific candidate has received
def get_votes():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

    # Get the total votes for each candidate
	cursor.execute("""
        SELECT c.name, COUNT(*) AS vote_count
        FROM votes v
        JOIN candidates c ON v.candidateId = c.candidateId
        GROUP BY c.name
    """)

    # Creates and returns a dictionary with the results of the query, key is candidate name, value is the number of votes
	candidate_votes = {name: count for name, count in cursor.fetchall()}

	conn.close()
	return candidate_votes

def delete_candidate(id):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  cursor.execute('DELETE FROM candidates WHERE candidateId = ?', (id,))

  conn.commit()
  conn.close

