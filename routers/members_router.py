import json

from flask import Blueprint, Response, request, Request, jsonify

from auth.token_manager import check_correct_token, get_token_info
from database.members_database import MembersDatabase
from database.teams_database import TeamDatabase
from responses import (
    response_not_correct_data,
    response_not_correct_token,
    response_not_owner,
    response_good,
)
from utils import check_request, not_owner_team, get_path_db
from flask_cors import CORS, cross_origin


class MembersRouter:

    def __init__(self, user_database: MembersDatabase) -> None:
        self.database = user_database
        self.blueprint = Blueprint("members", __name__)

        @self.blueprint.route("/members/add", methods=["POST"])
        @cross_origin()
        def members_add() -> tuple[Response, int]:
            return self.__add(request)

        @self.blueprint.route("/members/kick", methods=["POST"])
        @cross_origin()
        def members_kick() -> tuple[Response, int]:
            return self.__kick(request)

        @self.blueprint.route("/members", methods=["GET"])
        @cross_origin()
        def members_get() -> tuple[Response, int]:
            return self.__get(request)

        @self.blueprint.route("/members/team_id", methods=["GET"])
        @cross_origin()
        def members_getteam_id() -> tuple[Response, int]:
            return self.__get_team_id(request)

    def __get_team_id(self, request: Request) -> tuple[Response, int]:
        token = request.headers.get("Authorization")
        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        try:
            team_id = self.database.get_team_id_from_login(login)
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "not get"}}), 400
        return jsonify({"response": team_id}), 200

    def __add(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        team_db = TeamDatabase(get_path_db())
        login = get_token_info(token)["login"]
        if not_owner_team(data["team_id"], login, team_db):
            return response_not_owner()

        members_info = self.database.get(data["team_id"])
        if members_info is None:
            members_info = []
        team_info = team_db.get_team(data["team_id"])

        if team_info is None:
            return jsonify({"response": {"error": "Not been get"}}), 400

        if team_info.max_participants <= len(members_info):
            return jsonify({"response": {"error": "Limit members"}}), 400
        if data["login_member"] in members_info:
            return response_not_correct_data()
        try:
            self.database.add_user(data["team_id"], data["login_member"])
        except:
            return jsonify({"response": {"error": "User not added"}}), 400

        return response_good()

    def __kick(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        team_db = TeamDatabase(get_path_db())
        login = get_token_info(token)["login"]
        if not_owner_team(data["team_id"], login, team_db):
            return response_not_owner()

        try:
            self.database.kick_user(data["team_id"], data["login_member"])
        except:
            return jsonify({"response": {"error": "User not a kicked"}}), 400

        return response_good()

    def __get(self, request: Request) -> tuple[Response, int]:
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        team_db = TeamDatabase(get_path_db())
        login = get_token_info(token)["login"]
        if not_owner_team(request.args.get("team_id"), login, team_db):
            return response_not_owner()

        try:
            users = self.database.get(request.args.get("team_id"))
            if users is None:
                users = []
        except:
            return jsonify({"response": {"error": "Not been get"}}), 400

        return jsonify({"response": users}), 200
