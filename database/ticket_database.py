import sqlite3
from modules.invoice import Invoice


class TicketDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS tickets (
                owner_id TEXT,
                team_id TEXT,
                invoice_type TEXT,
                specialization TEXT,
                date TEXT
            );
            """
            )
        except Exception as e:
            conn.commit()
            conn.close()
            print(e)
            raise ValueError()
        conn.commit()
        conn.close()

    def create_invoice(self, invoice: Invoice) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            INSERT INTO tickets (owner_id, team_id, invoice_type, specialization, date) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    invoice.owner_id,
                    invoice.team_id,
                    invoice.invoice_type,
                    invoice.specialization,
                    invoice.date,
                ),
            )
        except Exception as e:
            conn.commit()
            conn.close()
            print(e)
            raise ValueError()
        conn.commit()
        conn.close()

    def remove_invoice(self, invoice: Invoice) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM tickets WHERE owner_id= ? AND team_id = ? AND invoice_type = ?
            """,
            (invoice.owner_id, invoice.team_id, invoice.invoice_type,),
        )

        conn.commit()
        conn.close()

    def get_invoices_for_team(self, team_id: str) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tickets WHERE team_id = ? AND invoice_type = ?
            """,
            (team_id, "to_team",),
        )
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        r = []
        for rr in result:
            r.append(Invoice(*rr).to_dict())
        return r

    def get_invoices_for_user(self, login: str) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tickets WHERE owner_id = ? AND invoice_type = ?
            """,
            (login, "to_user",),
        )
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        r = []
        for rr in result:
            r.append(Invoice(*rr).to_dict())
        return r

    def is_new_ticket(self, invoice: Invoice) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tickets WHERE owner_id = ?  AND team_id = ?
            """,
            (
                invoice.owner_id,
                invoice.team_id,
            ),
        )
        result = cursor.fetchone()
        conn.commit()
        conn.close()

        return result is None
