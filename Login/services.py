from Login import database


def username_exists(username: str) -> bool:
    "Checks if a username already exists"
    return database.get_username(username) is not None

def add_user(username: str, password: str) -> bool:
    "Adds a new user to the database"
    return database.add_user(username, password)

def password_strong(password: str) -> bool:
    "Checks if a password meets the strength requirements"
    if len(password) < 8:
        return False

    upper_letters = 0
    letters = 0
    digits = 0

    for char in password:
        if char.isdigit():
            digits += 1
        else:
            if char.isupper():
                upper_letters += 1
            letters += 1
    return upper_letters >= 1 and letters >= 1 and digits >= 1

def passwords_match(password: str, password_duplicate: str) -> bool:
    "Checks if password inputs match"
    return password == password_duplicate

def create_user(username: str, password: str, password_duplicate) -> bool:
    "Creates a new user in the database if username doesnt exist and password is strong and matches"
    if username_exists(username) or not password_strong(password) and passwords_match(password, password_duplicate):
        return False
    else:
        return add_user(username, password)

def verify_user(username: str, password: str) -> bool:
    "Checks if a username exists in the database and password is strong and matches"
    return database.verify_user(username, password)

