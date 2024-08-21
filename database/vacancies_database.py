from modules.vacancy import Vacancy
from database.manager_database import get_connection


class VacanciesDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    team_id TEXT,
                    hardskill TEXT,
                    specialization TEXT
                );
                """
            )
            conn.commit()

        except Exception as e:
            conn.commit()

            print(e)
            raise ValueError()

    def new_vacancy(self, vacancy: Vacancy) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO vacancies (team_id, hardskill, specialization) VALUES (?, ?, ?)
                """,
                (
                    vacancy.team_id,
                    vacancy.hardskill_str,
                    vacancy.specialization,
                ),
            )
            conn.commit()
        except Exception as e:
            conn.commit()
            print(e)
            raise ValueError()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM vacancies WHERE team_id = ? AND specialization = ?",
                (
                    vacancy.team_id,
                    vacancy.specialization,
                ),
            )

            conn.commit()
        except Exception as e:
            conn.commit()
            print(e)
            raise ValueError()

    def get_vacancies(self, specialization: str) -> list[dict]:

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM vacancies WHERE team_id = ?", (specialization,)
        )
        result = []
        for vacan in cursor.fetchall():
            result.append({"team_id": vacan[0], "hardskill": vacan[1], "specialization": vacan[2]})
        return result  # type: ignore
