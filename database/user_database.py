import sqlite3
from typing import Optional

from database.manager_database import get_connection
from modules.user import User


class UserDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                login TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                fullname TEXT DEFAULT('unknown'),
                telegram TEXT DEFAULT NULL,
                type TEXT DEFAULT NULL,
                hardskill TEXT DEFAULT NULL,
                softskill TEXT DEFAULT NULL,
                role TEXT,
                specialization TEXT DEFAULT NULL,
                description TEXT DEFAULT NULL,
                picture TEXT DEFAULT NULL
            );
            """
        )

        conn.commit()

    def insert_user(self, login: str, password: str, role: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (login, password, role)
                VALUES (?, ?, ?)
                """,
                (
                    login,
                    password,
                    role,
                ),
            )
        except:
            conn.commit()
            raise ValueError("base error")

        conn.commit()

    def get_user(self, login: str) -> Optional[User]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = cursor.fetchone()
        return User(*user) if user else None

    def update_user(self, user: User) -> None:

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE users
                SET fullname = ?, telegram = ?, type = ?, hardskill = ?, softskill = ?, role = ?, specialization = ?, description = ?, picture = ?
                WHERE login = ?
                """,
                (
                    user.username,
                    user.telegram,
                    user.user_type,
                    user.get_str_hardskills(),
                    user.get_str_softskills(),
                    user.role,
                    user.specialization,
                    user.description,
                    user.picture,
                    user.login,
                ),
            )
        except Exception as e:
            conn.commit()
            print(e)
            raise ValueError()
        conn.commit()

    def change_password(self, login: str, new_password: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            UPDATE users
            SET password = ?
            WHERE login = ?
            """,
                (new_password, login),
            )
        except Exception as e:
            conn.commit()
            print(e)
            raise ValueError()
        conn.commit()

    def get_all_users(self) -> list[User]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role='member'")
        users = cursor.fetchall()

        result = []
        for user in users:
            result.append(User(*user))
        return result
