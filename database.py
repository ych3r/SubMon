import sqlite3

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

    # TODO: create target

    # TODO: get target

    # TODO: update target

    # TODO: delete target

    # TODO: get subdomain

    # TODO: update subdomain