import sqlite3 as sql
import bcrypt

conn = sql.connect("users_credentials.db")

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS credentials (username TEXT UNIQUE, password TEXT)")


def register_user(username: str, password: str):
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sql.IntegrityError:
        return False
    except sql.OperationalError:
        cursor.execute("CREATE TABLE IF NOT EXISTS credentials (username TEXT UNIQUE, password TEXT)")
        return None

def verify_user(username: str, provided_password: str):
    cursor.execute("SELECT password FROM credentials WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        return False
    stored_hash = result[0]
    return check_password(stored_hash, provided_password)

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(stored_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)


def close_db():
    conn.close()
