from flask import Blueprint, Response, request, Request, jsonify

from auth.token_manager import check_correct_token, get_token_info
from database.members_database import MembersDatabase
from database.teams_database import TeamDatabase
from database.ticket_database import TicketDatabase
from database.user_database import UserDatabase
from database.vacancies_database import VacanciesDatabase
from responses import response_not_correct_token
from flask_cors import CORS, cross_origin

from utils import get_path_db


class SearchRouter:

    def __init__(
            self,
            user_db: UserDatabase,
            team_db: TeamDatabase,
            members_db: MembersDatabase,
            ticket_db: TicketDatabase,
    ):
        self.user_db = user_db
        self.team_db = team_db
        self.members_db = members_db
        self.titcket_db = ticket_db

        self.blueprint = Blueprint("search", __name__)


        @self.blueprint.route("/search", methods=["GET"])
        @cross_origin()
        def search() -> tuple[Response, int]:
            return self.__search(request)

    def buble_sort_users(self, users: [(float, str)]) -> [(float, str)]:
        well = True
        while well:
            well = False
            for i in range(len(users) - 1):
                if users[i + 1][0] > users[i][0]:
                    users[i], users[i + 1] = users[i + 1], users[i]
                    well = True
        return users

    def convert_users(self, users: [(float, str)]):
        result = []
        for user in users:
            result.append({"percent": user[0], "login": user[1]})
        return result

    def __search(self, request: Request) -> tuple[Response, int]:
        token = request.headers.get("Authorization")
        if not check_correct_token(token):
            return response_not_correct_token()
        login = get_token_info(token)["login"]
        current_user = self.user_db.get_user(login)
        try:
            if current_user.role == "owner":
                print(11)
                print(login)
                team_id = self.team_db.get_team_id_from_owner(login)
                print(team_id)
                users = self.user_db.get_all_users()

                users_not_sorting = []
                db_vac = VacanciesDatabase(get_path_db())
                print(team_id)
                vanacys = db_vac.get_vacancies(team_id)
                print(vanacys, 100)
                for user in users:
                    count_success = 0.0
                    count_vacan = 0
                    for vacan in vanacys:

                        for soft_skill in vacan["hardskill"].split(","):
                            if user is not None and user.softskill is not None and soft_skill in user.softskill:
                                count_success += 1
                            count_vacan += 1
                    if count_vacan == 0:
                        count_vacan = 1
                    users_not_sorting.append(
                         (
                             round(count_success / count_vacan * 100, 2),
                             user.login,
                         )
                     )

                return jsonify(self.convert_users(self.buble_sort_users(users_not_sorting))), 200
            else:
                teams = self.team_db.get_all_team()
                teams_not_sortings = []

                for team in teams:
                    count_success = 0.0

                    for soft_skill in str(team.get_dict()["hardskills"]).split(","):

                        if (
                                current_user.hardskill is not None
                                and soft_skill in current_user.hardskill
                        ):
                            count_success += 1
                    if current_user.hardskill is not None:
                        teams_not_sortings.append(
                        (
                            round(count_success / len(current_user.hardskill) * 100, 2),
                            team.team_id,
                            )
                        )
                    else:
                        teams_not_sortings.append(
                            (
                                round(count_success / 1 * 100, 2),
                                team.team_id,
                            )
                        )
                return jsonify(self.convert_users(self.buble_sort_users(teams_not_sortings))), 200
        except Exception as e:
            print(e)
            return jsonify({"response": []}), 200
