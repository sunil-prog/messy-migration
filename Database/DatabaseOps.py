import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'Database/users.db'

def get_db_connection():
    """
    Get a connection to the database.
    Returns:
        sqlite3.Connection: A connection to the database.
    """
    return sqlite3.connect(DB_PATH)

# --- User Queries --- #

def get_all_users():
    """
    Get all users from the database.
    Returns:
        list: A list of tuples, each containing user data.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()
            return users
    except sqlite3.Error as e:
        return {"error": str(e)}


def get_user_by_id(user_id):
    """
    Get a user by their ID.
    Args:
        user_id (int): The ID of the user to get.
    Returns:
        tuple: A tuple containing user data, or None if the user does not exist.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            return user
    except sqlite3.Error as e:
        return {"error": str(e)}

def create_user(name, email, password):
    """
    Create a new user in the database.
    Hashes the password before storing it in the database.
    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    Returns:
        int: The ID of the newly created user.
    """
    try:
        # Hash the password
        with get_db_connection() as conn:
            hashed_password = generate_password_hash(password)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        return {"error": "User with this email already exists"}
    except sqlite3.Error as e:
        return {"error": str(e)}

def update_user(user_id, name, email):
    """
    Update an existing user in the database.
    Args:
        user_id (int): The ID of the user to update.
        name (str): The new name of the user.
        email (str): The new email of the user.
    Returns:
        int: The number of rows updated.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            conn.commit()
            return cursor.rowcount
    except sqlite3.IntegrityError as e:
        return {"error": "User with this email already exists"}
    except sqlite3.Error as e:
        return {"error": str(e)}

def delete_user(user_id):
    """
    Delete a user from the database.
    Args:
        user_id (int): The ID of the user to delete.
    Returns:
        int: The number of rows deleted.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount
    except sqlite3.Error as e:
        return {"error": str(e)}

def search_user_by_name(name):
    """
    Search for users by their name.
    Args:
        name (str): The name to search for.
    Returns:
        list: A list of tuples, each containing user data.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
            users = cursor.fetchall()
            return users
    except sqlite3.Error as e:
        return {"error": str(e)}

def authenticate_user(email, password):
    """
    Authenticate a user by their email and password.
    Args:
        email (str): The email of the user.
        password (str): The password of the user.
    Returns:
        tuple: A tuple containing user data, or None if the user does not exist.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            return user[:3]
        return None
    except sqlite3.Error as e:
        return {"error": str(e)}