from database.manager_database import get_connection
from modules.organization import Organization


class OrganizationsDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                org_id TEXT,
                title TEXT,
                description TEXT,
                owner TEXT
            );
        """)

        conn.commit()

    def create_organization(self, org: Organization):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                    INSERT INTO organizations (org_id, title, description, owner) VALUES (?, ?, ?, ?)
                    """, (org.org_id, org.title, org.description, org.owner,))
        conn.commit()

    def get_organization(self, org_id: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                            SELECT * FROM organizations WHERE org_id = ?
                            """, (org_id,))
        return Organization(*cursor.fetchone())

    def remove_organization(self, org_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                        DELETE FROM organizations WHERE org_id = ?
                   """, (org_id,))

        conn.commit()