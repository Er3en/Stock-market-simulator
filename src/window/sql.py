import sqlite3
import hashlib
import os


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key


def verify_password(stored_password, provided_password):
    salt = stored_password[:16]
    key = stored_password[16:]
    new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return key == new_key


def store_user(username, password):
    conn = sqlite3.connect('../database/users.db')
    cursor = conn.cursor()

    salt = os.urandom(16)
    hashed_password = hash_password(password, salt)

    cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
    conn.commit()
    conn.close()


def verify_login(username, password):
    conn = sqlite3.connect('../database/users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password = result[0]
        return verify_password(stored_password, password)

    return False

