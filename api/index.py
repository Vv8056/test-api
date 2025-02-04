# from flask import Flask, jsonify
# from flask_cors import CORS
# import json

# app = Flask(__name__)
# CORS(app) #This will enable CORS for all routes

# # Load data from JSON file
# def load_data():
#     with open('data.json', 'r') as file:
#         return json.load(file)

# # GET all data
# @app.route('/users', methods=['GET'])
# def get_users():
#     data = load_data()
#     return jsonify(data)

# # GET a single user by ID
# @app.route('/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     data = load_data()
#     user = next((item for item in data if item["id"] == user_id), None)
#     if user:
#         return jsonify(user)
#     return jsonify({"error": "User not found"}), 404

# # GET a user's certificate by ID
# @app.route('/users/<int:user_id>/certificate', methods=['GET'])
# def get_user_certificate(user_id):
#     data = load_data()
#     user = next((item for item in data["users"] if item["id"] == user_id), None)
#     if user and "certificate" in user:
#         return jsonify(user["certificate"])
#     return jsonify({"error": "Certificate not found for this user"}), 404

# if __name__ == '__main__':
#     app.run(debug=False)


# from flask import Flask, jsonify, send_file
# from flask_cors import CORS
# import json

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Hardcoded paths (Replace with actual paths if needed)
# DATA_FILE = "data.json"
# CERTIFICATES_DIR = "certificates/"  # Ensure this folder exists in the same directory

# # Load data from JSON file
# def load_data():
#     try:
#         with open('DATA_FILE', 'r') as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError) as e:
#         print(f"Error loading JSON: {e}")
#         return {"users": []}  # Return an empty list if the file is missing or broken

# # GET all users
# @app.route('/users', methods=['GET'])
# def get_users():
#     data = load_data()
#     return jsonify(data.get("users", []))  # Ensure default empty list

# # GET a single user by ID
# @app.route('/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     data = load_data()
#     user = next((item for item in data.get("users", []) if item["id"] == user_id), None)
#     if user:
#         return jsonify(user)
#     return jsonify({"error": "User not found"}), 404

# # GET a user's certificate by ID
# @app.route('/users/<int:user_id>/certificate', methods=['GET'])
# def get_user_certificate(user_id):
#     data = load_data()
#     user = next((item for item in data.get("users", []) if item["id"] == user_id), None)
    
#     if not user:
#         return jsonify({"error": "User not found"}), 404
    
#     certificate = user.get("certificate")
    
#     if certificate:
#         return jsonify(certificate)
    
#     return jsonify({"error": "Certificate not found for this user"}), 404

# @app.route("/certificates/<filename>", methods=["GET"])
# def get_certificate(filename):
#     file_path = CERTIFICATES_DIR + filename  # Construct file path

#     try:
#         return send_file(file_path, as_attachment=True)
#     except FileNotFoundError:
#         return jsonify({"error": "Certificate file not found"}), 404

# if __name__ == '__main__':
#     app.run(debug=False)



# from flask import Flask, jsonify, send_file, abort
# from flask_cors import CORS
# import json
# import os

# app = Flask(__name__)
# CORS(app)  # Allow all origins (Consider restricting this in production)

# # Paths
# DATA_FILE = "data.json"
# CERTIFICATES_DIR = "certificates/"  # Ensure this folder exists

# # Load data from JSON file
# def load_data():
#     try:
#         with open(DATA_FILE, "r") as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError) as e:
#         print(f"Error loading JSON: {e}")
#         return {"users": []}  # Return an empty list if the file is missing or broken

# # GET all users
# @app.route("/users", methods=["GET"])
# def get_users():
#     data = load_data()
#     return jsonify(data.get("users", []))  # Ensure default empty list

# # GET a single user by ID
# @app.route("/users/<int:user_id>", methods=["GET"])
# def get_user(user_id):
#     data = load_data()
#     user = next((item for item in data.get("users", []) if item["id"] == user_id), None)
#     if user:
#         return jsonify(user)
#     return jsonify({"error": "User not found"}), 404

# # GET a user's certificate data
# @app.route("/users/<int:user_id>/certificate", methods=["GET"])
# def get_user_certificate(user_id):
#     data = load_data()
#     user = next((item for item in data.get("users", []) if item["id"] == user_id), None)

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     certificate = user.get("certificate")
#     if certificate:
#         return jsonify(certificate)

#     return jsonify({"error": "Certificate not found for this user"}), 404

# # Serve a PDF certificate file
# @app.route("/certificates/<filename>", methods=["GET"])
# def get_certificate(filename):
#     file_path = os.path.join(CERTIFICATES_DIR, filename)  # Construct file path properly

#     if os.path.exists(file_path):  
#         try:
#             return send_file(file_path, as_attachment=True)
#         except Exception as e:
#             print(f"Error sending file: {e}")  # Debugging log
#             return jsonify({"error": "Failed to serve the certificate"}), 500

#     return jsonify({"error": "Certificate file not found"}), 404

# # @app.route("/certificates/<filename>", methods=["GET"])
# # def get_certificate(filename):
# #     file_path = os.path.join(CERTIFICATES_DIR, filename)

# #     # Check if file exists before sending
# #     if not os.path.exists(file_path):
# #         return jsonify({"error": "Certificate file not found"}), 404

# #     try:
# #         return send_file(file_path, as_attachment=False)
# #     except Exception as e:
# #         print(f"Error sending file: {e}")  # Log error
# #         return jsonify({"error": "Internal Server Error"}), 500

# if __name__ == "__main__":
#     app.run(debug=False)




# new

from flask import Flask, jsonify, send_from_directory
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Hardcoded paths (Replace with actual paths if needed)
DATA_FILE = "data.json"
CERTIFICATES_DIR = os.path.join(os.getcwd(), "static", "certificates")  # Ensure this folder exists

# Load data from JSON file
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": []}

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    data = load_data()
    return jsonify(data.get("users", []))

# GET a single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    data = load_data()
    user = next((item for item in data.get("users", []) if item["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# GET a user's certificate data
@app.route("/users/<int:user_id>/certificate", methods=["GET"])
def get_user_certificate(user_id):
    data = load_data()
    user = next((item for item in data.get("users", []) if item["id"] == user_id), None)
    
    if user and "certificate" in user:
        return jsonify(user["certificate"])
    return jsonify({"error": "Certificate not found for this user"}), 404

# Serve a PDF certificate file
@app.route("/certificates/<filename>", methods=["GET"])
def get_certificate(filename):
    if os.path.exists(os.path.join(CERTIFICATES_DIR, filename)):
        return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)
    return jsonify({"error": "Certificate file not found"}), 404

if __name__ == "__main__":
    app.run(debug=False)
