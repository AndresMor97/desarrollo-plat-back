from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()


class UsuarioDTO(ma.Schema):
    """Schema para serializar datos de usuario."""
    id_usuario = fields.Int()
    nombre = fields.Str()
    email = fields.Email()
    estado = fields.Str()
    creado_en = fields.DateTime()
