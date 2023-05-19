from passlib.hash import pbkdf2_sha256
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('src/database/users.db')
cursor = conn.cursor()

# Retrieve all user records from the database
cursor.execute('SELECT id, username, password, salt FROM users')
users = cursor.fetchall()

# Iterate over the user records and hash the passwords
for user in users:
    user_id = user[0]
    username = user[1]
    password = user[2]
    salt = user[3]
    print(salt)
    # Encode the salt to bytes
    salt_bytes = salt.encode('utf-8')
    
    # Hash the password using pbkdf2_sha256
    hashed_password = pbkdf2_sha256.hash(password, salt=salt_bytes, rounds=100000)
    
    # Update the user record in the database with the new hashed password
    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
