import sqlite3

# Adds a vote to the database table 'votes'
def add_vote(userId: int, candidateId: int):
	conn = sqlite3.connect('voting.db')
	cursor = conn.cursor()

	cursor.execute('INSERT INTO votes (userId, candidateId) VALUES (?, ?)', (userId, candidateId))
	conn.commit()
	conn.close

# Retrieves all candidates from the database table 'candidates'
# Returns a dictionary where the key is the candidate name and the value is the image path
def get_candidates():
	conn = sqlite3.connect('voting.db')
	cursor = conn.cursor()

	candidates = {}
	cursor.execute('SELECT * FROM candidates')
	rows = cursor.fetchall()

	for row in rows:
		candidates.update({row[1]: row[2]})

	conn.close

	return candidates

# Gets the candidate ID from the database based on the candidate name
# Takes the candidate name as a parameter and returns the candidate ID
def get_candidate_id(candidate_name: str):
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()

    candidates = {}
    cursor.execute('SELECT candidateId FROM candidates WHERE name = ?', (candidate_name,))
    rows = cursor.fetchall()

    conn.close
    return rows[0][0]

# Checks if a user has already voted
# Takes the username as a parameter and returns a tuple
# The first element in the tuple is a boolean indicating if the user has voted (True) or not (False)
# The second element in the tuple is the user ID
def check_if_voted(user_name: str):
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()

    cursor.execute("SELECT userId FROM users WHERE username = ?", (user_name,))
    record = cursor.fetchone()
	
    if len(record) > 0:
        user_id = record[0]
        cursor.execute("SELECT * FROM votes WHERE userId = ?", (user_id,))
		
        vote = cursor.fetchone()
		
        conn.close
        return ((vote != None), user_id)
    else:
        conn.close
        return None