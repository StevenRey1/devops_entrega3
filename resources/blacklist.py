from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from models import Blacklist, db
from schemas import BlacklistSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import datetime

blacklist_schema = BlacklistSchema()

class HealthCheckResource(Resource):
    def get(self):
        return {"status": "ok"}, 200



class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            #data['app_uuid'] = str(uuid.uuid4()) #Generate a UUID for the app if it doesn't provide one.  Not required according to the document.
            validated_data = blacklist_schema.load(data)
            #validated_data = data #Comment the above line and uncomment this one if you're not using Marshmallow validation.

            email = validated_data['email']
            app_uuid = validated_data['app_uuid']
            blocked_reason = validated_data.get('blocked_reason')  # Get with default None
            request_ip = request.remote_addr
            #created_at = datetime.datetime.utcnow() #This will be populated automatically since it's defined in the model.

            # Create a new Blacklist object
            blacklist_entry = Blacklist(
                email=email,
                app_uuid=app_uuid,
                blocked_reason=blocked_reason,
                request_ip=request_ip,
                #created_at=created_at
            )

            db.session.add(blacklist_entry)
            db.session.commit()

            return {"message": "Email agregado a la lista negra"}, 201

        except ValidationError as err:
            return {"error": err.messages}, 400
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {"error": str(e)}, 500


class BlacklistCheckResource(Resource):
    @jwt_required()
    def get(self, email):
        blacklist_entry = Blacklist.query.filter_by(email=email).first()
        if blacklist_entry:
            return {"is_blacklisted": True, "reason": blacklist_entry.blocked_reason}, 200
        else:
            return {"is_blacklisted": False, "reason": None}, 200