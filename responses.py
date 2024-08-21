from flask import Response, jsonify


def response_not_found() -> tuple[Response, int]:
    return jsonify({"response": {"error": "Data not found"}}), 400


def response_not_correct_data() -> tuple[Response, int]:
    return jsonify({"response": {"error": "Data not correct"}}), 400


def response_not_correct_token() -> tuple[Response, int]:
    return jsonify({"response": {"error": "Token not correct"}}), 400


def internal_server_error() -> tuple[Response, int]:
    return jsonify({"response": {"error": "Internal server error"}}), 500


def response_not_owner() -> tuple[Response, int]:
    return jsonify({"response": {"error": "You are not owner this team"}}), 400


def response_good() -> tuple[Response, int]:
    return jsonify({"response": "good"}), 200