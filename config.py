import os

class Config:
    # Ajustar con credenciales de MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345@localhost/MyMoney'
    SQLALCHEMY_TRACK_MODIFICATIONS = False