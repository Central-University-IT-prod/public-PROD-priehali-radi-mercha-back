import json

from flask import Blueprint, Response, Request, jsonify, request
from flask_cors import CORS, cross_origin  # type: ignore

from auth.token_manager import check_correct_token, get_token_info
from database.vacancies_database import VacanciesDatabase
from modules.vacancy import Vacancy
from responses import response_not_correct_data, response_not_correct_token
from utils import check_request


class VacancyRouter:
    def __init__(self, vacan_database: VacanciesDatabase) -> None:
        self.database = vacan_database
        self.blueprint = Blueprint("vanacy", __name__)

        @self.blueprint.route("/vacancy", methods=["POST"])
        @cross_origin()
        def team_create() -> tuple[Response, int]:
            return self.__create_vanacy(request)

        @self.blueprint.route("/vacancy", methods=["GET"])
        @cross_origin()
        def team_get() -> tuple[Response, int]:
            return self.__get_vanacy(request)

        @self.blueprint.route("/vacancy", methods=["DELETE"])
        @cross_origin()
        def team_remove() -> tuple[Response, int]:
            return self.__remove_vanacy(request)

    def __create_vanacy(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            self.database.new_vacancy(
                Vacancy(data["team_id"], data["hardskill"], data["specialization"])
            )
        except:
            return jsonify({"response": {"error": "Vacany not created"}}), 400
        return jsonify({"response": "good"}), 200

    def __get_vanacy(self, request: Request) -> tuple[Response, int]:

        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            vacancies = self.database.get_vacancies(request.args.get("team_id"))
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Vacany not created"}}), 400
        return jsonify({"response": vacancies}), 200

    def __remove_vanacy(self, request: Request) -> tuple[Response, int]:
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        self.database.delete_vacancy(
            Vacancy(data["team_id"], "", data["specialization"])
        )
        return jsonify({"response": "good"}), 200
