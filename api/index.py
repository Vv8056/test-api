from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) #This will enable CORS for all routes

# Load data from JSON file
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

# GET all data
@app.route('/users', methods=['GET'])
def get_users():
    data = load_data()
    return jsonify(data)

# GET a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data = load_data()
    user = next((item for item in data if item["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# GET a user's certificate by ID
@app.route('/users/<int:user_id>/certificate', methods=['GET'])
def get_user_certificate(user_id):
    data = load_data()
    user = next((item for item in data["users"] if item["id"] == user_id), None)
    if user and "certificate" in user:
        return jsonify(user["certificate"])
    return jsonify({"error": "Certificate not found for this user"}), 404

if __name__ == '__main__':
    app.run(debug=False)
