from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()


class CategoriaDTO(ma.Schema):
    """Schema para serializar y validar categorías."""
    id_categoria = fields.Int()
    nombre = fields.Str()
    tipo = fields.Str()
