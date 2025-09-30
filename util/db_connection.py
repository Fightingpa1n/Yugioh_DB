from flask import g
import json
import mysql.connector
import os

from util.config import get_config

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

    def execute_script(self, script_text:str):
        cursor = self.connection.cursor()
        try:
            results = cursor.execute(script_text, multi=True)
            if results:
                for result in results:
                    try: result.fetchall()
                    except: pass
            self.connection.commit()
        finally:
            cursor.close()

def get_db() -> DBConnection:
    """Get the database connection."""
    if 'db' not in g:
        try:
            config = get_config()
            db_config = config.get("db", {})
            db_host = db_config.get("host")
            db_port = db_config.get("port")
            db_name = db_config.get("name")
            db_user = db_config.get("user")
            db_password = db_config.get("password")
            g.db = DBConnection(db_host, db_port, db_name, db_user, db_password)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise e
    return g.db

def get_db_connection() -> DBConnection:
    """Get the database connection for outside flask app stuff"""
    config = get_config()
    db_config = config.get("db", {})
    db_host = db_config.get("host")
    db_port = db_config.get("port")
    db_name = db_config.get("name")
    db_user = db_config.get("user")
    db_password = db_config.get("password")
    return DBConnection(db_host, db_port, db_name, db_user, db_password)
    
    
