from flask import Blueprint, request
from src.controllers.categoria_controller import (
    listar_categorias_logic, 
    crear_categoria_logic,
    eliminar_categoria_logic,
    obtener_saldos_por_categoria_logic # <-- Nueva importación
)
from src.utils.auth_middleware import token_required

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias', methods=['GET'])
@token_required
def get_categorias(current_user):
    tipo = request.args.get('tipo')
    return listar_categorias_logic(tipo, current_user)

@categoria_bp.route('/categorias', methods=['POST'])
@token_required
def post_categoria(current_user):
    data = request.get_json()
    return crear_categoria_logic(data, current_user)

@categoria_bp.route('/categorias/<int:id_categoria>', methods=['DELETE'])
@token_required
def delete_categoria(current_user, id_categoria):
    return eliminar_categoria_logic(id_categoria, current_user)

# <-- NUEVO ENDPOINT PARA SALDOS POR CATEGORÍA -->
@categoria_bp.route('/categorias/saldos', methods=['GET'])
@token_required
def get_saldos_categorias(current_user):
    return obtener_saldos_por_categoria_logic(current_user)