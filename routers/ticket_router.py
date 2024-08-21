import json

from flask import Blueprint, Response, request, Request, jsonify

from auth.token_manager import check_correct_token, get_token_info
from database.teams_database import TeamDatabase
from database.ticket_database import TicketDatabase
from database.user_database import UserDatabase
from responses import (
    response_not_correct_data,
    response_not_correct_token,
    response_not_owner,
    response_good,
)
from utils import check_request, get_path_db, not_owner_team
from modules.invoice import Invoice
from datetime import datetime
from flask_cors import CORS, cross_origin


class TicketRouter:
    def __init__(
        self,
        tiket_database: TicketDatabase,
        team_database: TeamDatabase,
        user_database: UserDatabase,
    ) -> None:
        self.database = tiket_database
        self.team_database = team_database
        self.user_database = user_database
        self.blueprint = Blueprint("ticket", __name__)

        @self.blueprint.route("/ticket", methods=["POST"])
        @cross_origin()
        def team_create() -> tuple[Response, int]:
            return self.__ticket_create(request)

        @self.blueprint.route("/ticket", methods=["GET"])
        @cross_origin()
        def team_get() -> tuple[Response, int]:
            return self.__get_tickets(request)

        @self.blueprint.route("/ticket/delete", methods=["POST"])
        @cross_origin()
        def team_delete() -> tuple[Response, int]:
            return self.__remove_ticket(request)

    def __ticket_create(self, request: Request) -> tuple[Response, int]:
        """
        json = {
            "team_id": str - команда, над которой происходит операция
            "user_login": str - кого добавить в команду, если отправляет owner
            "specialization": str - специализация
        }
        """

        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")
        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        user_info = self.user_database.get_user(login)

        if user_info is None:
            return response_not_correct_data()

        if user_info.role == "owner":
            if not_owner_team(data["team_id"], login, self.team_database):
                return response_not_owner()

            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            invoice = Invoice(
                data["user_login"],
                data["team_id"],
                "to_user",
                data["specialization"],
                date,
            )

            # user = self.user_database.get_user(invoice.owner_id)
            # if user is None:
            #   return response_not_correct_data()

            # if user.role == "owner":
            #    return response_not_correct_data()

            # if not self.database.is_new_ticket(invoice):
            #    return response_not_correct_data()

            self.database.create_invoice(invoice)
        else:
            date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            invoice = Invoice(
                login, data["team_id"], "to_team", data["specialization"], date
            )

            # if not self.database.is_new_ticket(invoice):
            #     return response_not_correct_data()
            self.database.create_invoice(invoice)

        return response_good()

    def __get_tickets(self, request: Request) -> tuple[Response, int]:

        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        user_info = self.user_database.get_user(login)

        if user_info is None:
            return response_not_correct_data()

        if user_info.role == "owner":
            team_id = request.args.get("team_id")
            result = self.database.get_invoices_for_team(team_id)

        else:
            result = self.database.get_invoices_for_user(login)

        return jsonify({"response": result}), 200

    def __remove_ticket(self, request: Request) -> tuple[Response, int]:
        """
        json = {
            "team_id": str - команда, над которой происходит операция
            "login_member": str - днные о пользователе в тикете
            "specialization": str - специализация
        }
        """

        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        user_info = self.user_database.get_user(login)

        if user_info is None:
            return response_not_correct_data()

        team_id = data.get("team_id")
        owner_id = data.get("login_member")
        specialization = data.get("specialization")

        if (
            not check_request(request)
            or team_id is None
            or owner_id is None
            or specialization is None
        ):
            return response_not_correct_data()

        if user_info.role == "owner":
            self.database.remove_invoice(Invoice(owner_id, team_id, "to_user", specialization, ""))
            self.database.remove_invoice(Invoice(owner_id, team_id, "to_team", specialization, ""))
        else:
            self.database.remove_invoice(Invoice(owner_id, team_id, "to_user", specialization, ""))
            self.database.remove_invoice(Invoice(owner_id, team_id, "to_team", specialization, ""))

        return jsonify({"response": "good"}), 200
