from flask import Blueprint, request
from src.controllers.transaccion_controller import (
    crear_transaccion_logic, 
    obtener_saldo_logic,
    listar_historial_logic,
    obtener_estadisticas_gastos_logic, # <-- Nueva importación (HU 5)
    eliminar_transaccion_logic         # <-- Nueva importación (HU 6)
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

# HU 4: Historial de Transacciones
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

# -------------------------------------------------------------
# Rutas del Sprint 3
# -------------------------------------------------------------

# HU 5: Gráfico de Estadísticas de Gastos
@transaccion_bp.route('/estadisticas/gastos', methods=['GET'])
@token_required
def get_estadisticas_gastos(current_user):
    return obtener_estadisticas_gastos_logic(current_user)

# HU 6: Eliminar Transacción
# Usamos <int:id_transaccion> para capturar el ID directamente de la URL
@transaccion_bp.route('/transacciones/<int:id_transaccion>', methods=['DELETE'])
@token_required
def delete_transaccion(current_user, id_transaccion):
    return eliminar_transaccion_logic(id_transaccion, current_user)