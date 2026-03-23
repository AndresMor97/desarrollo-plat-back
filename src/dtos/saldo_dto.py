from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class SaldoDTO(ma.Schema):
    id_usuario = fields.Int()
    total_ingresos = fields.Float()
    total_gastos = fields.Float()
    saldo_actual = fields.Float()