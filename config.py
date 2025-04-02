import os

class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@database-2.c5qeceeaoqys.us-east-2.rds.amazonaws.com:5432/database_1")
    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///blacklist.db")  # SQLite por defecto
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "super-secret")  # ¡Cambiar en producción!

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Example SQLite for testing
    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///blacklist.db")  # SQLite por defecto
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@database-2.c5qeceeaoqys.us-east-2.rds.amazonaws.com:5432/database_1")
    JWT_SECRET_KEY = "dev-secret" #Don't use this in production.

class ProductionConfig(Config):
    # ...configuración específica para producción...
    pass

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.JWT_SECRET_KEY