from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()


class TransaccionDTO(ma.Schema):
    """Schema para validar y serializar transacciones."""
    id_transaccion = fields.Int(dump_only=True)
    id_usuario = fields.Int(dump_only=True)
    fecha_transaccion = fields.DateTime(dump_only=True)

    monto = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, error="El monto debe ser mayor a 0")
    )
    descripcion = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )
    tipo = fields.Str(
        required=True,
        validate=validate.OneOf(["ingreso", "gasto"])
    )
    id_categoria = fields.Int(allow_none=True)
