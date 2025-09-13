import sqlite3
from typing import Any
from schemas import TargetCreate, TargetRead, Subdomain

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table_target()
        self.create_table_subdomain()

    def create_table_target(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS target (
                name        TEXT PRIMARY KEY,
                program_url TEXT,
                notes       TEXT
            )
        """)
    
    def create_table_subdomain(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS subdomain (
                name        TEXT PRIMARY KEY,
                status      TEXT,
                title       TEXT,
                target_name TEXT,
                FOREIGN KEY (target_name) REFERENCES target(name) ON DELETE CASCADE
            )
        """)

    # create target
    def create_target(self, domain: str, target: TargetCreate) -> dict[str, Any]:
        self.cur.execute("""
            INSERT OR IGNORE INTO target
            VALUES (:name, :program_url, :notes)
        """,
        {
            "name": domain,
            **target.model_dump(),
        }
        )
        self.conn.commit()
        return {"domain": domain}

    # get target
    def get_target(self, domain: str) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM target
            WHERE name = ?
        """, (domain,))
        row = self.cur.fetchone()

        return {
            "name": row[0],
            "program_url": row[1],
            "notes": row[2],
            "subdomains": self.get_subdomains(domain)
        } if row else None

    # update target
    def update_target(self, domain: str, target: TargetCreate) -> dict[str, Any] | None:
        self.cur.execute("""
            UPDATE target
            SET program_url = :program_url,
                notes = :notes
            WHERE name = :name
        """,
        {
            "name": domain,
            **target.model_dump()
        })
        self.conn.commit()
        return self.get_target(domain)

    # delete target
    def delete_target(self, domain: str):
        self.cur.execute("""
            DELETE FROM target
            WHERE name = ?
        """, (domain,))
        self.conn.commit()

    # get subdomain
    def get_subdomains(self, domain: str) -> list[Subdomain]:
        self.cur.execute("""
            SELECT * FROM subdomain
            WHERE target_name = ?
        """, (domain,))
        rows = self.cur.fetchall()
        return [
            Subdomain(
                name=row[0],
                status=row[1],
                title=row[2],
                target_name=row[3]
            ) for row in rows
        ] if rows else []

    # add subdomain
    def add_subdomains(self, domain: str, subdomain_list: list[Subdomain]) -> list[Subdomain]:
        # Add each subdomain in the list
        for subdomain in subdomain_list:
            self.cur.execute("""
                INSERT OR IGNORE INTO subdomain
                VALUES (:name, :status, :title, :target_name)
            """,
            {
            **subdomain.model_dump(),
            "target_name": domain
            })
        self.conn.commit()
        return subdomain_list

    def close(self):
        self.conn.close()