from flask import Flask, g

from webapp.api import database

app = Flask(__name__)

#Flask app
app.register_blueprint(database.bp)

@app.route('/')
def home():
    return "Webapp is running!"