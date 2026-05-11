from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class CategoriaDTO(ma.Schema):
    id_categoria = fields.Int(dump_only=True)
    id_usuario = fields.Int(dump_only=True) 
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=50))

# DTO ACTUALIZADO: Para el saldo neto por categoría
class SaldoCategoriaDTO(ma.Schema):
    id_categoria = fields.Int(dump_only=True)
    nombre = fields.Str(dump_only=True)
    total_ingresos = fields.Float(dump_only=True)
    total_gastos = fields.Float(dump_only=True)
    saldo_total = fields.Float(dump_only=True) # <-- El resultado final (Ingresos - Gastos)