from flask import request, Blueprint, send_file
from responses import *
from utils import *
import base64
from io import BytesIO
from PIL import Image  # type: ignore
import json
from auth.token_manager import check_correct_token, get_token_info
import os
from database.teams_database import TeamDatabase
from flask_cors import CORS, cross_origin


class TeamImage:
    def __init__(self, team_db: TeamDatabase) -> None:
        self.blueprint = Blueprint("team_image", __name__)
        self.database = team_db


        @self.blueprint.route("/team/image", methods=["POST"])
        @cross_origin()
        def upload_image() -> tuple[Response, int]:
            return self.__upload_image()

        @self.blueprint.route("/team/image", methods=["GET"])
        @cross_origin()
        def get_image() -> tuple[Response, int]:
            return self.__get_image()

        @self.blueprint.route("/team/image", methods=["DELETE"])
        def delete_image() -> tuple[Response, int]:
            return self.__delete_image()

    def __upload_image(self) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token).get("login")
        team_id = data.get("team_id")
        encoded_string = data.get("image")

        if (login is None) or (encoded_string is None) or (team_id is None):
            return response_not_correct_token()

        if not_owner_team(team_id, login, self.database):
            return response_not_owner()

        try:
            image = Image.open(BytesIO(base64.b64decode(encoded_string)))
            image.save(f"images/team_images/{team_id}.png", "PNG")
        except Exception as e:
            print(e)
            return jsonify({"response": "error"}), 400

        return jsonify({"response": "ok"}), 200

    def __get_image(self) -> tuple[Response, int]:
        token = request.headers.get("Authorization")
        data: dict = json.loads(request.data.decode())

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token).get("login")
        team_id = data.get("team_id")

        if (login is None) or (team_id is None):
            return response_not_correct_token()

        if not_owner_team(team_id, login, self.database):
            return response_not_owner()

        path = f"images/team_images/{team_id}.png"

        if not os.path.exists(path):
            return jsonify({"response": "error"}), 400

        return send_file(path, mimetype="image/png"), 200

    def __delete_image(self) -> tuple[Response, int]:
        token = request.headers.get("Authorization")
        data: dict = json.loads(request.data.decode())

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token).get("login")
        team_id = data.get("team_id")

        if (team_id is None) or (login is None):
            return response_not_correct_data()

        if not_owner_team(team_id, login, self.database):
            return response_not_owner()

        if not os.path.exists(f"images/team_images/{team_id}.png"):
            return jsonify({"response": "error"}), 400

        try:
            os.remove(f"images/team_images/{team_id}.png")
        except:
            return jsonify({"response": "error"}), 400

        return jsonify({"response": "ok"}), 200
