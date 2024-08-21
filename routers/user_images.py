from flask import request, Blueprint, send_file
from responses import *
from utils import *
import base64
from io import BytesIO
from PIL import Image
import json
from auth.token_manager import check_correct_token, get_token_info
import os
from flask_cors import CORS, cross_origin


class UserImage:
    def __init__(self) -> None:
        self.blueprint = Blueprint("user_image", __name__)


        @self.blueprint.route("/profile/image", methods=["POST"])
        @cross_origin()
        def upload_image() -> tuple[Response, int]:
            return self.__upload_image()

        @self.blueprint.route("/profile/image", methods=["GET"])
        @cross_origin()
        def get_image() -> tuple[Response, int]:
            return self.__get_image()

        @self.blueprint.route("/profile/image", methods=["DELETE"])
        @cross_origin()
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
        encoded_string = data.get("image")

        if (login is None) or (encoded_string is None):
            return response_not_correct_token()

        try:
            image = Image.open(BytesIO(base64.b64decode(encoded_string)))
            image.save(f"images/user_images/{login}.png", "PNG")
        except Exception as e:
            print(e)
            return jsonify({"response": "error"}), 400

        return jsonify({"response": "ok"}), 200

    def __get_image(self) -> tuple[Response, int]:
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token).get("login")
        if login is None:
            return response_not_correct_token()

        path = f"images/user_images/{login}.png"

        if not os.path.exists(path):
            return jsonify({"response": "error"}), 400

        return send_file(path, mimetype="image/png"), 200

    def __delete_image(self) -> tuple[Response, int]:
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token).get("login")
        if login is None:
            return response_not_correct_token()

        if not os.path.exists(f"images/user_images/{login}.png"):
            return jsonify({"response": "error"}), 400

        try:
            os.remove(f"images/user_images/{login}.png")
        except:
            return jsonify({"response": "error"}), 400

        return jsonify({"response": "ok"}), 200
