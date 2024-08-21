import sqlite3
from typing import Optional

from database.manager_database import get_connection


class MembersDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                team_id TEXT,
                member_login TEXT
            );
            """
        )

        conn.commit()

    def get_team_id_from_login(self, login: str) -> Optional[str]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT team_id FROM members WHERE member_login=?
            """,
            (login,),
        )
        info = cursor.fetchone()
        if info is None:
            return None

        team_id = info[0]
        return team_id  # type: ignore

    def add_user(self, team_id: str, member_login: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            INSERT INTO members (team_id, member_login)
            VALUES (?, ?)
            """,
                (
                    team_id,
                    member_login,
                ),
            )
        except Exception as e:
            conn.commit()
            print(e)
            raise ValueError()
        conn.commit()

    def kick_user(self, team_id: str, member_login: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM members WHERE team_id = ? AND member_login = ?
            """,
            (
                team_id,
                member_login,
            ),
        )
        conn.commit()

    def get(self, team_id: str) -> Optional[list[str]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT member_login FROM members WHERE team_id = ?", (team_id,))
        members = cursor.fetchall()

        members = [member[0] for member in members]
        return members if members else None
