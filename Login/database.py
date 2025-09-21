import sqlite3
from operator import truediv

import bcrypt

DATABASE_NAME = 'user_data.db'
def initialise_database():
    """Intialises the database and creates a user table if it doesn't exist."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        password_hash TEXT NOT NULL,
        walk_streak INTEGER DEFAULT 0,
        work_streak INTEGER DEFAULT 0,''')
    conn.commit()

def add_user(username, password):
    """Adds a new user to the database."""
    salt = bycrypt.gensalt()
    hashed_password = bcrypt.hashpw(password('utf-8'), salt)
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password.decode('utf-8')))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def get_user(username):
    """Returns a user from the database."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

def verify_user(username, password):
    """Verifies a user's password against the database."""
    user = get_user(username)
    if user:
        password_hash = user[2]
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)
    else:
        return False
