from flask import g
import json
import mysql.connector
import os


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(REPO_ROOT, "config.json")

class DBConnection:
    """Database connection class. Handles connecting to the database and executing queries."""
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
        )

    def __del__(self):
        self.close()

    def close(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
        except Exception:
            pass
    
    def query(self, sql, params=()):
        cur = self.connection.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()
    
    def execute(self, sql, params=()):
        cur = self.connection.cursor()
        try:
            cur.execute(sql, params)
            last_id = cur.lastrowid
            self.connection.commit()
            return last_id
        finally:
            cur.close()

    def execute_script(self, script_text: str):
        cur = self.connection.cursor()
        try:
            # naive split is fine for our simple DDL (no stored procs)
            statements = [s.strip() for s in script_text.split(";")]
            for stmt in statements:
                if not stmt:
                    continue
                # skip single-line comments
                if stmt.startswith("--") or stmt.startswith("#"):
                    continue
                cur.execute(stmt)
            self.connection.commit()
        finally:
            cur.close()


def get_db():
    """Get the database connection."""
    if 'db' not in g:
        
        with open(CONFIG_PATH) as config_file:
            config = json.load(config_file)
            db_config = config.get("db", {})
            db_host = db_config.get("host")
            db_port = db_config.get("port")
            db_name = db_config.get("name")
            db_user = db_config.get("user")
            db_password = db_config.get("password")
        g.db = DBConnection(db_host, db_port, db_name, db_user, db_password)
    return g.db

