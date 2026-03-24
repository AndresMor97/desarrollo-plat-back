from datetime import datetime
from src.models.transaccion_model import db # Importamos la instancia de db centralizada

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # El default de Python asegura que siempre se guarde la fecha de creación
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación opcional: permite acceder a las transacciones desde el objeto usuario
    # transacciones = db.relationship('Transaccion', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'