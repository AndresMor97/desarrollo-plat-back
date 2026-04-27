import os


class Config:
    """Configuración de la aplicación."""
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345@localhost/MyMoney'
    SECRET_KEY = 'tu_llave_secreta_super_segura_123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
