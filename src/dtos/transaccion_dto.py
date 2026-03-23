from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class TransaccionDTO(ma.Schema):
    # Validaciones del DTO
    id_usuario = fields.Int(required=True)
    monto = fields.Float(required=True, validate=validate.Range(min=0.01))
    descripcion = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    tipo = fields.Str(required=True, validate=validate.OneOf(["ingreso", "gasto"]))
    id_categoria = fields.Int(allow_none=True)