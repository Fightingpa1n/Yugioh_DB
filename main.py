from flask import Flask, g

from webapp.api import init

app = Flask(__name__)

#Flask app
app.register_blueprint(init.bp)

@app.route('/')
def home():
    return "Webapp is running!"

def run_app():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    run_app()