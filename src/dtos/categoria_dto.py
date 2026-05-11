from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class CategoriaDTO(ma.Schema):
    id_categoria = fields.Int(dump_only=True)
    id_usuario = fields.Int(dump_only=True) # Protegido, lo asignará el backend
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    tipo = fields.Str(required=True, validate=validate.OneOf(["ingreso", "gasto"]))

# NUEVO DTO: Para estructurar la respuesta del saldo acumulado por cada categoría
class SaldoCategoriaDTO(ma.Schema):
    id_categoria = fields.Int(dump_only=True)
    nombre = fields.Str(dump_only=True)
    tipo = fields.Str(dump_only=True)
    total_acumulado = fields.Float(dump_only=True)