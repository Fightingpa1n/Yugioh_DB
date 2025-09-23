from flask import Blueprint, request
from webapp.util import db_connection
import os

bp = Blueprint('api', __name__, url_prefix='/db')

#Add Database routes here (endpoints that interact with the database for like debug and stuff)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INIT_SQL_PATH = os.path.join(REPO_ROOT, "db", "init.sql")

@bp.route('/init', methods=['GET', 'POST'])
def init_db():
    db:db_connection.DBConnection = db_connection.get_db() #get db connection

    #run initialization script (db/init/init.sql) which then runs all other scripts in sequence to set up the database
    with open(INIT_SQL_PATH, 'r') as f:
        init_script = f.read()
        db.execute_script(init_script)

    return {"status": "success", "message": "Database initialized"}, 200


@bp.route('/add_test_data', methods=['GET', 'POST'])
def add_test_data():
    db:db_connection.DBConnection = db_connection.get_db() #get db connection

    db.execute("INSERT INTO cards (id, type_id, name, description) VALUES (1, 1, 'Blue-Eyes White Dragon', 'This legendary dragon is a powerful engine of destruction. Virtually invincible, very few have faced this awesome creature and lived to tell the tale.')")
    db.execute("INSERT INTO users (id, username) VALUES (1, 'testuser')")
    db.execute("INSERT INTO user_cards (user_id, card_id, quantity) VALUES (1, 1, 3)")

    return {"status": "success", "message": "Test data added"}, 200


@bp.route('/cards', methods=['GET'])
def get_cards():
    db:db_connection.DBConnection = db_connection.get_db() #get db connection

    cards = db.query("SELECT * FROM cards")
    return {"status": "success", "cards": cards}, 200


@bp.route('/testUserCards', methods=['GET'])
def get_test_user_cards():
    db:db_connection.DBConnection = db_connection.get_db() #get db connection

    user_cards = db.query("""
        SELECT uc.user_id, c.id, c.name, c.description, uc.quantity
        FROM user_cards uc
        JOIN cards c ON uc.card_id = c.id
        WHERE uc.user_id = %s
    """, (1,))

    return {"status": "success", "user_cards": user_cards}, 200