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



from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allow all origins (Consider restricting this in production)

# Paths
DATA_FILE = "data.json"
# CERTIFICATES_DIR = "certificates/"  # Ensure this folder exists
# Folder where PDFs are stored
PDF_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'certificates')

# Load data from JSON file
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return {"users": []}  # Return an empty list if the file is missing or broken
        
# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    data = load_data()
    return jsonify(data.get("users", []))  # Ensure default empty list

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

    if not user:
        return jsonify({"error": "User not found"}), 404
    certificate = user.get("certificate")
    if certificate:
        return jsonify(certificate)
    return jsonify({"error": "Certificate not found for this user"}), 404

# GET a user's experience details
@app.route("/users/<int:user_id>/experience", methods=["GET"])
def get_user_experience(user_id):
    data = load_data()
    user = next((u for u in data.get("users", []) if u.get("id") == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    experience = user.get("experience", [])
    if not experience:
        return jsonify({"error": "Experience data not available for this user"}), 404
    return jsonify(experience)

# GET a user's education details
@app.route("/users/<int:user_id>/education", methods=["GET"])
def get_user_education(user_id):
    data = load_data()
    user = next((u for u in data.get("users", []) if u.get("id") == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    education = user.get("education", [])
    if not education:
        return jsonify({"error": "Education data not available for this user"}), 404
    return jsonify(education)
    
# Serve a PDF certificate file
@app.route('/list-pdfs', methods=['GET'])
def list_pdfs():
    """List all PDF files in the 'pdfs' folder."""
    try:
        files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
        return jsonify({"pdf_files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/view-cert/<filename>', methods=['GET'])
def view_pdf(filename):
    """Serve a PDF file for viewing."""
    return send_from_directory(PDF_FOLDER, filename)

if __name__ == "__main__":
    os.makedirs(PDF_FOLDER, exist_ok=True)  # Ensure the 'pdfs' folder exists
    app.run(debug=False)
