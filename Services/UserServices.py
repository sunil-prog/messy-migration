""" 
    UserServices.py
    This file contains the services for the user management system.
"""

import Database.DatabaseOps as db
from flask import jsonify
import validators

# --- User Services --- #

def check_valid_email(email):
    """
    Check if the email is valid.
    Args:
        email (str): The email to check.
    """
    return validators.email(email)

def get_all_users():
    """
    Get all users from the database.
    Returns:
        list: A list of tuples, each containing user data.
    """
    users = db.get_all_users()
    if "error" in users:
        return jsonify(users), 500
    return jsonify(users), 200

def get_user_by_id(user_id):
    """
    Get a user by their ID.
    Args:
        user_id (int): The ID of the user to get.
    Returns:
        tuple: A tuple containing user data, or None if the user does not exist.
    """
    user = db.get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    if "error" in user:
        return jsonify(user), 500
    return jsonify(user), 200

def create_user(name, email, password):
    """
    Create a new user in the database.
    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    Returns:
        json: A JSON object containing the user ID or an error message.
    """
    if not name or not email or not password:
        return jsonify({"error": "Please provide a name, email and password to create a user"}), 400
    if not check_valid_email(email):
        return jsonify({"error": "Please provide a valid email"}), 400
    user = db.create_user(name, email, password)
    if isinstance(user, int):
        return jsonify({"message": "User created successfully", "user_id": user}), 201
    if "error" in user:
        return jsonify(user), 400

def update_user(user_id, name, email):
    """
    Update an existing user in the database.
    Args:
        user_id (int): The ID of the user to update.
        name (str): The new name of the user.
        email (str): The new email of the user.
    """
    if not name or not email:
        return jsonify({"error": "Please provide a name and email to update"}), 400
    if not check_valid_email(email):
        return jsonify({"error": "Please provide a valid email"}), 400
    result = db.update_user(user_id, name, email)
    if result == 0:
        return jsonify({"error": "User not found"}), 404
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400
    return jsonify({"message": "User updated successfully"}), 200

def delete_user(user_id):
    """
    Delete a user from the database.
    Args:
        user_id (int): The ID of the user to delete.
    """
    result = db.delete_user(user_id)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500
    if result == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200

def search_user_by_name(name):
    """
    Search for users by their name.
    Args:
        name (str): The name to search for.
    """
    if not name:
        return jsonify({"error": "Please provide a name to search for"}), 400
    users = db.search_user_by_name(name)
    if "error" in users:
        return jsonify(users), 500
    if not users:
        return jsonify({"error": "No users found with this name"}), 404
    return jsonify(users), 200

def login(email, password):
    """
    Authenticate a user by their email and password.
    Args:
        email (str): The email of the user.
        password (str): The password of the user.
    """
    user = db.authenticate_user(email, password)
    if isinstance(user, dict) and "error" in user:
        return jsonify(user), 400
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"message": "Login successful", "user": user}), 200

