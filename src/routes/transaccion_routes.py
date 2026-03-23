from flask import Blueprint, request
from src.controllers.transaccion_controller import crear_transaccion_logic

transaccion_bp = Blueprint('transaccion_bp', __name__)

@transaccion_bp.route('/transacciones', methods=['POST'])
def post_transaccion():
    data = request.get_json()
    return crear_transaccion_logic(data)