from database.manager_database import get_connection


class OrganizationsMembersDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS organizations_members (
                        org_id TEXT,
                        member_login TEXT
                    );
                """)

        conn.commit()

    def add_member(self, org_id: str, member_login: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                            INSERT INTO organizations_members (org_id, member_login) VALUES (?, ?)
                        """, (org_id, member_login,))
        conn.commit()

    def remove_member(self, org_id, member_login):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                        DELETE FROM organizations_members WHERE org_id = ? AND member_login = ?
                        """, (org_id, member_login, ))
        conn.commit()

    def get_members(self, org_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT member_login FROM organizations_members WHERE org_id = ?
                                """, (org_id,))
        members = cursor.fetchall()
        conn.commit()
        result = []
        for member in members:
            result.append(member[0])
        return result