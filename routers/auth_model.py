from functools import update_wrapper
from responses import response_not_correct_data
from auth.token_manager import generate
from database.user_database import UserDatabase
from utils import to_md5, check_request
from flask import (
    Blueprint,
    Response,
    Request,
    request,
    jsonify,
    make_response,
    current_app,
)
from flask_cors import CORS, cross_origin
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


class RegisterRoute:

    def __init__(self, user_database: UserDatabase) -> None:
        self.database = user_database
        self.blueprint = Blueprint("register", __name__)

        @self.blueprint.route("/auth/register", methods=["POST"])
        @cross_origin()
        def register() -> tuple[Response, int]:
            return self.__register(request)

    def __register(self, request: Request) -> tuple[Response, int]:

        if not check_request(request):
            return response_not_correct_data()

        json = request.get_json()
        login, password, role = json["login"], json["password"], json["role"]

        if (
            (len(login) < 3 or len(login) > 30)
            or (len(password) < 6 or len(password) > 30)
            or role not in ["owner", "member"]
        ):
            return response_not_correct_data()

        try:
            encoded_password = to_md5(password)
        except:
            return response_not_correct_data()

        try:
            self.database.insert_user(login, encoded_password, role)
        except:
            return jsonify({"response": {"error": "User already exists"}}), 400

        response = jsonify({"response": generate(login)})

        return response, 200


class LoginRoute:
    def __init__(self, user_database: UserDatabase) -> None:
        self.database = user_database
        self.blueprint = Blueprint("login", __name__)

        @self.blueprint.route("/auth/login", methods=["POST"])
        @cross_origin()
        def auth() -> tuple[Response, int]:
            return self.__auth(request)

    def __auth(self, request: Request) -> tuple[Response, int]:

        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return response_not_correct_data()

        json = request.get_json()

        login = json["login"]
        password = to_md5(json["password"])

        user_info = self.database.get_user(login)

        if user_info is None or user_info.password != password:
            return jsonify({"response": {"error": "Not correct data"}}), 400
        return jsonify({"response": generate(login)}), 200
