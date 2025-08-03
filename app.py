# Import necessary modules from Flask and the UserServices operations
from flask import Flask, request, jsonify
import Services.UserServices as UserOps

# Initialize the Flask application
app = Flask(__name__)

# Home route to verify the server is running
@app.route('/')
def home():
    return "User Management System"

# Route to get all users (GET request)
@app.route('/users', methods=['GET'])
def get_all_users():
    return UserOps.get_all_users()

# Route to get a specific user by user_id (GET request)
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    return UserOps.get_user_by_id(user_id)

# Route to create a new user (POST request)
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()  # Get JSON data from request body
    name = user_data['name']
    email = user_data['email']
    password = user_data['password']
    return UserOps.create_user(name, email, password)

# Route to update an existing user's name and email (PUT request)
@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()  # Get JSON data from request body
    name = user_data['name']
    email = user_data['email']
    return UserOps.update_user(user_id, name, email)

# Route to delete a user by user_id (DELETE request)
@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserOps.delete_user(user_id)

# Route to search users by name (GET request with query parameter)
@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    return UserOps.search_user_by_name(name)

# Route to handle user login (POST request)
@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()  # Get JSON data from request body
    email = login_data['email']
    password = login_data['password']
    return UserOps.login(email, password)

    
# Run the Flask app on host 0.0.0.0 and port 5009 in debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)