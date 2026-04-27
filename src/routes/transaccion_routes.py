from flask import Blueprint, request
from src.controllers.transaccion_controller import (
    crear_transaccion_logic,
    obtener_saldo_logic,
    listar_historial_logic,
    obtener_estadisticas_gastos_logic,
    eliminar_transaccion_logic,
)
from src.utils.auth_middleware import token_required

transaccion_bp = Blueprint('transaccion_bp', __name__)


@transaccion_bp.route('/transacciones', methods=['POST'])
@token_required
def post_transaccion(current_user):
    """Crea una nueva transacción para el usuario autenticado."""
    data = request.get_json()
    return crear_transaccion_logic(data, current_user)


@transaccion_bp.route('/transacciones', methods=['GET'])
@token_required
def get_historial(current_user):
    """Lista el historial de transacciones del usuario autenticado."""
    return listar_historial_logic(current_user)


@transaccion_bp.route('/saldo', methods=['GET'])
@token_required
def get_saldo(current_user):
    """Calcula y devuelve el saldo del usuario autenticado."""
    return obtener_saldo_logic(current_user)


@transaccion_bp.route('/estadisticas/gastos', methods=['GET'])
@token_required
def get_estadisticas_gastos(current_user):
    """Devuelve estadísticas de gastos agrupadas por categoría."""
    return obtener_estadisticas_gastos_logic(current_user)


@transaccion_bp.route('/transacciones/<int:id_transaccion>', methods=['DELETE'])
@token_required
def delete_transaccion(current_user, id_transaccion):
    """Elimina una transacción existente del usuario autenticado."""
    return eliminar_transaccion_logic(id_transaccion, current_user)
