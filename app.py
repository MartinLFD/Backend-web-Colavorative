from flask import Flask, request, jsonify
from models import db
from flask_migrate import Migrate
from flask_cors import CORS
from models import Role, User, Camping, Reservation, Review, Site


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///camping.db"



db.init_app(app)
Migrate(app, db)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return "<h1> Camping API </h1>"

@app.route("/role", methods=["POST"]) # METHOD POST PARA ROLE
def role():
    data = request.get_json()
    role = Role()
    role.name = data["name"]

    db.session.add(role)
    db.session.commit()

    return "Usuario creado"

@app.route("/role", methods=["GET"]) # METHOD GET PARA TRAER TODOS LOS ROLES
def get_roles(): 
    roles = Role.query.all()
    roles = list(map(lambda role: role.serialize(), roles))

    return jsonify(roles)
    
if __name__== "__main__":
    app.run(host = "localhost", port=4000, debug=True)




# Endpoints a hacer ( User, Camping, Reservation, Review, Site) 
# POST - GET (methods)  