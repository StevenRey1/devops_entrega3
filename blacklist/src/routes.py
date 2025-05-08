from config import Config
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from models import Blacklist, db
from functools import wraps

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Decorador para verificar el token de autorización
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Verificando token de autorización...")
        token = request.headers.get('Authorization')
        if not token:
            print("Token de autorización no proporcionado")
            response = jsonify({"error": "Token de autorización es requerido"})
            response.status_code = 401
            return response
        if token != f"Bearer {Config.AUTH_TOKEN}":
            print("Token inválido")
            response = jsonify({"error": "Token de autorización no válido"})
            response.status_code = 403
            return response
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 404

class BlacklistResource(Resource):

    # Endpoint POST para agregar un email a la lista negra
    @token_required
    def post(self):
        data = request.get_json()
        email = data.get('email')
        app_uuid = data.get('app_uuid')
        blocked_reason = data.get('blocked_reason', '')

        if not email or not app_uuid:
            print("Email o app_uuid no proporcionados")
            response = jsonify({"message": "Email and app_uuid are required"})
            response.status_code = 400
            return response
        
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        new_entry = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason, ip_address=client_ip)
        db.session.add(new_entry)
        db.session.commit()
        print(f"Email {email} added to blacklist with reason: {blocked_reason}")
        
        response = jsonify({"message": "Email added to blacklist", "body": new_entry.to_dict()})
        response.status_code = 201
        return response

    # Endpoint GET para verificar si un email está en la lista negra
    @token_required
    def get(self, email):
        entry = Blacklist.query.filter_by(email=email).first()
        if not entry:
            print(f"Email {email} not found in blacklist")
            response = jsonify({"blacklisted": False})
            response.status_code = 200
            return response
        
        print(f"Email {email} found in blacklist with reason: {entry.blocked_reason}")
        response = jsonify({"blacklisted": True, "reason": entry.blocked_reason})
        response.status_code = 200
        return response

# Registrar el recurso de la API
api.add_resource(BlacklistResource, "/blacklists", "/blacklists/<string:email>")
