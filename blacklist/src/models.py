from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Agregar valor por defecto

    def to_dict(self):
        """Método para convertir el objeto en un diccionario serializable."""
        return {
            'id': self.id,
            'email': self.email,
            'app_uuid': self.app_uuid,
            'blocked_reason': self.blocked_reason,
            'ip_address': self.ip_address
        }