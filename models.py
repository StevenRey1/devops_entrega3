from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import datetime

db = SQLAlchemy()  # Inicializar db fuera de la app factory

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    request_ip = db.Column(db.String(45), nullable=False) # IPv6 support
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
