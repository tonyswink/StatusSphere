from functools import wraps
from flask import request, jsonify, current_app

def bearer_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Missing Authorization header"}), 401

        token_parts = auth_header.split(' ')
        if len(token_parts) != 2:
            return jsonify({"message": "Invalid Authorization header format"}), 401

        token_type, token_value = token_parts
        if token_type != "Bearer":
            return jsonify({"message": "Invalid token type. Expected 'Bearer'"}), 401

        if token_value != current_app.config['API_KEY']:
            return jsonify({"message": "Invalid API token"}), 401

        return f(*args, **kwargs)
    return decorated_function
