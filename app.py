from flask import Flask

from database.members_database import MembersDatabase
from database.organizations_database import OrganizationsDatabase
from database.organizations_members_database import OrganizationsMembersDatabase
from database.ticket_database import TicketDatabase
from database.vacancies_database import VacanciesDatabase
from routers import auth_model, profile_update, team_router, user_images, team_images
from routers.organizations_router import OrganizationRouter
from routers.search_router import SearchRouter
from routers.ticket_router import TicketRouter
from routers.vacancy_router import VacancyRouter
from utils import get_path_db
from database.user_database import UserDatabase
from database.teams_database import TeamDatabase
from routers.members_router import MembersRouter

app = Flask(__name__)
user_database = UserDatabase(get_path_db())
teams_database = TeamDatabase(get_path_db())
members_database = MembersDatabase(get_path_db())
ticket_database = TicketDatabase(get_path_db())
vacancy_database = VacanciesDatabase(get_path_db())
organizations_database = OrganizationsDatabase(get_path_db())
organizations_members_database = OrganizationsMembersDatabase(get_path_db())

user_database.create_table()

register_toute = auth_model.RegisterRoute(user_database)
login_route = auth_model.LoginRoute(user_database)
profile_update_route = profile_update.ProfileUpdateRouter(user_database)

image_router = user_images.UserImage()
image_team_router = team_images.TeamImage(teams_database)

search_router = SearchRouter(
    user_database, teams_database, members_database, ticket_database
)
organization_router = OrganizationRouter(organizations_database, organizations_members_database)
team_create_router = team_router.TeamCreateRouter(teams_database)
team_get_router = team_router.TeamGetRouter(teams_database)
team_update_router = team_router.TeamUpdateRouter(teams_database)
team_remove_router = team_router.TeamRemoveRouter(teams_database)

members_router = MembersRouter(members_database)
vacancy_router = VacancyRouter(vacancy_database)
ticket_router = TicketRouter(ticket_database, teams_database, user_database)

app.register_blueprint(register_toute.blueprint)
app.register_blueprint(login_route.blueprint)
app.register_blueprint(profile_update_route.blueprint)
app.register_blueprint(team_create_router.blueprint)
app.register_blueprint(team_get_router.blueprint)
app.register_blueprint(team_update_router.blueprint)
app.register_blueprint(team_remove_router.blueprint)
app.register_blueprint(image_router.blueprint)
app.register_blueprint(image_team_router.blueprint)
app.register_blueprint(members_router.blueprint)
app.register_blueprint(ticket_router.blueprint)
app.register_blueprint(search_router.blueprint)
app.register_blueprint(vacancy_router.blueprint)
app.register_blueprint(organization_router.blueprint)

if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)
