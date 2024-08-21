import json
from auth.token_manager import get_token_info, check_correct_token
from database.user_database import UserDatabase
from responses import (
    response_not_correct_data,
    response_not_correct_token,
    internal_server_error,
)
from utils import check_request
from flask import Blueprint, Request, request, jsonify, Response
from flask_cors import CORS, cross_origin


class ProfileUpdateRouter:
    def __init__(self, user_database: UserDatabase):
        self.database = user_database
        self.blueprint = Blueprint("profile", __name__)

        @self.blueprint.route("/profile", methods=["PATCH"])
        @cross_origin()
        def profile() -> tuple[Response, int]:
            return self.__update(request)

        @self.blueprint.route("/profile", methods=["GET"])
        @cross_origin()
        def get_profile() -> tuple[Response, int]:
            return self.__get(request)

        @self.blueprint.route("/profile/<user_login>", methods=["GET"])
        @cross_origin()
        def get_other_profile(user_login: str) -> tuple[Response, int]:
            return self.__get_other(request, user_login)

    def __update(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        parametrs = "password telegram type hardskill softskill role description picture username specialization"

        user = self.database.get_user(login)

        if user is None:
            return internal_server_error()

        for key, val in data.items():
            if key in parametrs:
                setattr(user, key, val)

        self.database.update_user(user)

        updated_user = self.database.get_user(login)
        if updated_user is None:
            return internal_server_error()

        return jsonify(updated_user.get_dict()), 200

    def __get(self, request: Request) -> tuple[Response, int]:

        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        user = self.database.get_user(login)

        if user is None:
            return internal_server_error()

        return jsonify(user.get_dict()), 200

    def __get_other(self, request: Request, user_login: str) -> tuple[Response, int]:

        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        user = self.database.get_user(user_login)

        if user is None:
            return internal_server_error()

        return jsonify(user.get_dict()), 200
