from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from resources.blacklist import BlacklistResource, BlacklistCheckResource, HealthCheckResource
from config import config_by_name, key
from models import db
import uuid


def create_app(config_name):
    application = Flask(__name__)
    application.config.from_object(config_by_name[config_name])
    db.init_app(application)  # Inicializar SQLAlchemy con la app
    return application

# Aquí renombramos la variable principal a `application`
application = create_app('dev')  # o 'prod'
api = Api(application)
jwt = JWTManager(application)

# Inicializar base de datos
with application.app_context():
    db.create_all()

api.add_resource(BlacklistResource, '/blacklists')
api.add_resource(BlacklistCheckResource, '/blacklists/<string:email>')
api.add_resource(HealthCheckResource, '/health')

@application.route("/token", methods=["GET"])  # Usualmente es POST, pero GET es útil para probar.
def create_token():
    # Simplemente devolvemos el token estático.  En un caso real, aquí estaría la lógica de login
    with application.app_context():  # Necesario para usar create_access_token fuera del contexto de la app
        access_token = create_access_token(identity="admin")
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    application.run(port=5000, debug=True)