import json
import time
from uuid import uuid4

from flask import Blueprint, Response, Request, request, jsonify

from auth.token_manager import check_correct_token, get_token_info
from modules.team import Team
from responses import (
    response_not_correct_data,
    response_not_correct_token,
    internal_server_error,
    response_not_owner,
)
from utils import check_request, not_owner_team
from database.teams_database import TeamDatabase
from flask_cors import CORS, cross_origin


class TeamCreateRouter:
    def __init__(self, team_database: TeamDatabase) -> None:
        self.database = team_database
        self.blueprint = Blueprint("team_create", __name__)

        @self.blueprint.route("/team/create", methods=["POST"])
        @cross_origin()
        def team_create() -> tuple[Response, int]:
            return self.__create_team(request)

    def __create_team(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        team_id = str(uuid4())
        login = get_token_info(token)["login"]

        if not_owner_team(team_id, login, self.database):
            return response_not_owner()

        name = data["name"]
        if len(name) < 4 or len(name) > 30:
            return response_not_correct_data()
        created_at = str(round(time.time()))

        try:
            self.database.insert_team(Team(team_id, login, name, created_at, 3, '', data['description']))
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Team not create"}}), 400
        return jsonify({"response": team_id}), 200


class TeamGetRouter:
    def __init__(self, team_database: TeamDatabase) -> None:
        self.database = team_database
        self.blueprint = Blueprint("team_get", __name__)

        @self.blueprint.route("/team", methods=["GET"])
        @cross_origin()
        def team_get() -> tuple[Response, int]:
            return self.__get_team(request)

    def __get_team(self, request: Request) -> tuple[Response, int]:
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        team_id = request.args.get("team_id")

        if team_id is None:
            return response_not_correct_data()

        try:
            team_info = self.database.get_team(team_id)
            if team_info is None:
                return response_not_correct_data()
        except:
            return jsonify({"response": {"error": "Team not found"}}), 400

        return jsonify({"response": team_info.get_dict()}), 200


class TeamUpdateRouter:
    def __init__(self, team_database: TeamDatabase) -> None:
        self.database = team_database
        self.blueprint = Blueprint("team_update", __name__)

        @self.blueprint.route("/team", methods=["PATCH"])
        @cross_origin()
        def team_create() -> tuple[Response, int]:
            return self.__team_update(request)

    def __team_update(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        team_id = data.get("team_id")

        if team_id is None:
            return response_not_correct_data()

        if not_owner_team(team_id, login, self.database):
            return response_not_owner()

        team = self.database.get_team(data["team_id"])
        if team is None:
            return internal_server_error()
        team_dict = team.get_dict()
        parametrs = ["name", "hardskills", "max_participants"]
        for key, val in data.items():
            if key in parametrs:
                if key == "name":
                    if len(val.strip()) < 4 or len(val.strip()) > 30:
                        return response_not_correct_data()
                team_dict[key] = val

        try:
            self.database.update_team(Team(**team_dict))
        except Exception as e:
            return response_not_correct_data()

        updated_team = self.database.get_team(data["team_id"])
        if updated_team is None:
            return internal_server_error()

        team_info = updated_team.get_dict()
        return jsonify({"response": team_info}), 200


class TeamRemoveRouter:
    def __init__(self, team_database: TeamDatabase) -> None:
        self.database = team_database
        self.blueprint = Blueprint("team_remove", __name__)

        @self.blueprint.route("/team", methods=["DELETE"])
        @cross_origin()
        def team_remove() -> tuple[Response, int]:
            return self.__team_remove(request)

    def __team_remove(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        team_id = data.get("team_id")

        if team_id is None:
            return response_not_correct_data()

        if not_owner_team(team_id, login, self.database):
            return response_not_owner()

        try:
            self.database.delete_team(data["team_id"])
        except:
            return jsonify({"response": {"error": "Not correct team id"}}), 400

        return jsonify({"response": "good"}), 400
