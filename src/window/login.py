from passlib.hash import pbkdf2_sha256
import hashlib
import sqlite3


def verify_password(stored_password, provided_password, salt):
    print(salt)
    password = provided_password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    # Hash the provided password with the given salt
    hashed_provided_password = pbkdf2_sha256.hash(password, salt=salt_bytes, rounds=100000)
    print(hashed_provided_password, stored_password)
    return stored_password == hashed_provided_password


def verify_login(username, password):
    conn = sqlite3.connect('src/database/users.db')
    cursor = conn.cursor()

    query = "SELECT password, salt FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password, salt = result
        return verify_password(stored_password, password, salt)

    return False


def print_users_table():
    conn = sqlite3.connect('src/database/users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()




