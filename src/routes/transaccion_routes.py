from flask import Blueprint, request
from src.controllers.transaccion_controller import (
    crear_transaccion_logic, 
    obtener_saldo_logic,
    listar_historial_logic
)
from src.utils.auth_middleware import token_required

transaccion_bp = Blueprint('transaccion_bp', __name__)

# HU 1: Crear Transacción
@transaccion_bp.route('/transacciones', methods=['POST'])
@token_required
def post_transaccion(current_user):
    # Fíjate que le pasamos el current_user al controlador
    data = request.get_json()
    return crear_transaccion_logic(data, current_user)

# HU 4: Historial de Transacciones (NUEVA)
@transaccion_bp.route('/transacciones', methods=['GET'])
@token_required
def get_historial(current_user):
    return listar_historial_logic(current_user)

# HU 2: Obtener Saldo
@transaccion_bp.route('/saldo', methods=['GET'])
@token_required
def get_saldo(current_user):
    # Eliminamos el request.args.get('id_usuario')
    # ¡La seguridad la maneja el middleware!
    return obtener_saldo_logic(current_user)