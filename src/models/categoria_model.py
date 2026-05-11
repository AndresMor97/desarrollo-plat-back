from src.models.transaccion_model import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Nueva columna conectada al usuario. nullable=True permite las categorías por defecto
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True) 
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.Enum('ingreso', 'gasto'), nullable=False)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'