from flask import Flask
from models import db
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///camping.db"



db.init_app(app)
Migrate(app, db)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return "<h1> Camping API </h1>"

if __name__== "__main__":
    app.run(host = "localhost", port=4000, debug=True)