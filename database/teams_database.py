import sqlite3
import datetime

from database.manager_database import get_connection
from modules.team import Team
from typing import Optional, Any


class TeamDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                team_id TEXT PRIMARY KEY,
                owner TEXT,
                name TEXT NOT NULL,
                created_at TEXT,
                max_participants INTEGER DEFAULT(3),
                hardskills TEXT DEFAULT NULL,
                description TEXT
            );
            """
        )

        conn.commit()

    def insert_team(self, team: Team) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            INSERT INTO teams (team_id, owner, name, created_at, max_participants, hardskills, description) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    team.team_id,
                    team.owner,
                    team.name,
                    team.created_at_str,
                    team.max_participants,
                    team.hardskills,
                    team.description,
                ),
            )
        except Exception as e:
            print(e)
            conn.commit()
            raise ValueError("ooops")
        conn.commit()

    def get_team(self, team_id: str) -> Optional[Team]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE team_id = ?", (team_id,))
        team = cursor.fetchone()
        conn.close()
        return Team(*team) if team else None

    def update_team(self, team: Team) -> None:
        conn = get_connection()
        cursor = conn.cursor()


        try:
            cursor.execute(
                """
            UPDATE teams
            SET name = ?, created_at = ?, hardskills = ?, max_participants = ?
            WHERE team_id = ?
            """,
                (
                    team.name,
                    team.created_at_str,
                    ",".join(team.hardskills),
                    team.max_participants,
                    team.team_id,
                ),
            )
        except Exception as e:
            print(e)
            conn.commit()
            raise ValueError("ooops")
        conn.commit()

    def delete_team(self, team_id: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teams WHERE team_id = ?", (team_id,))

        conn.commit()

    def get_team_id_from_owner(self, owner: str) -> str:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT team_id FROM teams WHERE owner = ?", (owner,))
        team_id = cursor.fetchone()[0]
        conn.commit()

        return team_id  # type: ignore

    def get_all_team(self) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams")
        teams = cursor.fetchall()
        conn.close()
        result = []

        for team in teams:
            result.append(Team(*team))

        return result
