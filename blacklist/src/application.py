from flask import Flask
from models import db
from config import Config
import os

def create_app():
    from routes import api_bp

    print("Iniciando aplicación...")
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    print(f"Conectando a la base de datos en {application.config['SQLALCHEMY_DATABASE_URI']}")
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)

    # Crear tablas automáticamente al iniciar la app
    with application.app_context():
        print("Iniciando creación de tablas...")
        db.create_all()
        print("Tablas creadas correctamente.")

    # Registrar Blueprint
    application.register_blueprint(api_bp)
    return application

application = create_app()

if __name__ == "__main__": 
    print("Creando la aplicación...")
    application.run(host="0.0.0.0", port=5000, debug=True)

