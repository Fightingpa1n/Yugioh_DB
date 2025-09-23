from flask import g
import json
import mysql.connector
import os


CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config.json')

class DBConnection:
    """Database connection class. Handles connecting to the database and executing queries."""
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.connection = mysql.connector.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

    def __del__(self):
        self.close()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
    
    def query(self, query, params=()):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        self.connection.commit()
        return result
    
    def execute(self, sql, params=()):
        cur = self.connection.cursor()
        cur.execute(sql, params)
        last_id = cur.lastrowid
        self.connection.commit()
        cur.close()
        return last_id
    
    def execute_many(self, sql):
        cur = self.connection.cursor()
        cur.execute(sql, multi=True)
        self.connection.commit()
        cur.close()
    
    


def get_db():
    """Get the database connection."""
    if 'db' not in g:
        
        with open(CONFIG_PATH) as config_file:
            config = json.load(config_file)
            db_host = config.get("db_host")
            db_port = config.get("db_port")
            db_name = config.get("db_name")
            db_user = config.get("db_user")
            db_password = config.get("db_password")
        g.db = DBConnection(db_host, db_port, db_name, db_user, db_password)
    return g.db

