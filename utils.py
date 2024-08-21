import hashlib
from flask import Request

from database.teams_database import TeamDatabase


def check_request(request: Request) -> bool:
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return False
    return True


def get_path_db() -> str:
    return "database/database.db"


def to_md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def not_owner_team(team_id: str, login: str, team_db: TeamDatabase) -> bool:
    return False
    try:
        team_info = team_db.get_team(team_id)
        if team_info is None:
            return False
        return team_info.owner != login
    except:
        return False
