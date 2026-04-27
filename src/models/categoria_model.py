from src.models.transaccion_model import db


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.Enum('ingreso', 'gasto'), nullable=False)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
