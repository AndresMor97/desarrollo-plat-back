from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class CategoriaDTO(ma.Schema):
    id_categoria = fields.Int(dump_only=True)
    id_usuario = fields.Int(dump_only=True) # Protegido, lo asignará el backend
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    # ¡Eliminamos la validación del campo 'tipo' por completo!

# DTO: Para estructurar la respuesta del saldo acumulado por cada categoría
class SaldoCategoriaDTO(ma.Schema):
    id_categoria = fields.Int(dump_only=True)
    nombre = fields.Str(dump_only=True)
    tipo_transaccion = fields.Str(dump_only=True) # <-- Cambiamos 'tipo' por 'tipo_transaccion'
    total_acumulado = fields.Float(dump_only=True)