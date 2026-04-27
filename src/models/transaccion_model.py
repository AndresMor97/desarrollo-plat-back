from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Transaccion(db.Model):
    __tablename__ = 'transacciones'

    id_transaccion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_categoria = db.Column(db.Integer, nullable=True)
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_transaccion = db.Column(db.Date, default=datetime.utcnow)
    tipo = db.Column(db.Enum('ingreso', 'gasto'), nullable=False)
