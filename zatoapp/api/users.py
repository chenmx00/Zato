from flask import Blueprint, request, jsonify
from zatoapp.db import add_user, get_user
from flask_cors import CORS
from datetime import datetime

users_api_v1 = Blueprint(
    'users_api_v1', 'users_api_v1', url_prefix='/api/v1/users')
CORS(users_api_v1)

def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    raise AssertionError("Invalid input for type", field)

@users_api_v1.route('/addUser', methods=["POST"])
def api_post_addUser():
    """
    add a new user to the system from the registration
    """
    post_data = request.get_json()
    try:
        name = expect(post_data.get('name'), str, 'name')
        phone = expect(post_data.get('phone'), str, 'phone')
        email = expect(post_data.get('email'), str, 'email')
        add_user(name, email, phone)
        new_user = get_user(email)
        return jsonify({"new_user_added": new_user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_api_v1.route('/getUser', methods=['GET'])
def api_get_getUser():
    post_data = request.get_json()
    try:
            email = expect(post_data.get('email'), str, 'email')
            results = get_user(email)
            response_object = {
                "user_record": results
            }
            return jsonify(response_object), 200
    except Exception as e:
        response_object = {
            "error": str(e)
        }
        return jsonify(response_object), 400
