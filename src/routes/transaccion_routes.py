from flask import Blueprint, request
from src.controllers.transaccion_controller import crear_transaccion_logic, obtener_saldo_logic

transaccion_bp = Blueprint('transaccion_bp', __name__)

@transaccion_bp.route('/transacciones', methods=['POST'])
def post_transaccion():
    data = request.get_json()
    return crear_transaccion_logic(data)

@transaccion_bp.route('/saldo', methods=['GET'])
def get_saldo():
    # Se espera: /api/saldo?id_usuario=1
    id_user = request.args.get('id_usuario')
    if not id_user:
        return {"message": "Falta el id_usuario"}, 400
    return obtener_saldo_logic(id_user)