"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Empresa

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret cad auno deberia cmabiar esto a algo alarog"  # Change this!
# 11 diego  ====> adsfausdfhiasudfhiasudhfiuashdfiuasdhfi
# aaaaa
# bicicleta === bicicletaaaaaa
# marron === marronaaaaaa
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# INICO DE CODIGO

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
@jwt_required()
def handle_hello():
    all_users = User.query.all()

    print(all_users)
    results = list(map(lambda user: user.serialize(),all_users))
    print(results)

    response_body = {
        "msg": "leer los usuarios"
    }

    return jsonify(results), 200


@app.route('/empresa', methods=['GET'])
def get_empresas():
    all_empresas = Empresa.query.all()
    results = list(map(lambda enterprise: enterprise.serialize(),all_empresas))

    return jsonify(results), 200

@app.route('/empresa/<int:empresa_id>', methods=['GET'])
def get_empresa(empresa_id):
    empresa = Empresa.query.filter_by(id=empresa_id).first()
    return jsonify(empresa.serialize()), 200

@app.route('/empresa', methods=['POST'])
def create_empresa():
    # leer los datos que me envia la solicitud(body)
    data = request.json 
    print(data)
    if not 'ciudad' in data:
        return jsonify('ldebes enviar la ciduad'), 400
    if data['ciudad'] == "":
         return jsonify('la ciudad no debe ser vacia'), 400
    print(data.get('ciudad'))
    print(data['ciudad'])
    # crear una empresa nueva
    company = Empresa(**data)
    db.session.add(company)
    db.session.commit()

    response_body = {
        "msg": "debo crear empresa"
    }

    return jsonify(response_body), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "ese correo no existe"}), 401
    print(email)
    print(user)
    
    if password != user.password:
        return jsonify({"msg": "la calve es incorrecta"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# FIN DE CODIGO

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
