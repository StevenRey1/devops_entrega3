import os

class Config:
    DB_USER = os.getenv('RDS_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('RDS_PASSWORD', 'password')
    DB_HOST = os.getenv('RDS_HOSTNAME', 'localhost')
    DB_PORT = os.getenv('RDS_PORT', '5432')
    DB_NAME = os.getenv('RDS_DB_NAME', 'blacklist_db')
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_TOKEN = "mi_token_predefinido"  # Token estático