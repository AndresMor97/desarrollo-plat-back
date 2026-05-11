from flask import Blueprint, request
from src.controllers.categoria_controller import listar_categorias_logic, crear_categoria_logic
from src.utils.auth_middleware import token_required

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias', methods=['GET'])
@token_required # <-- Ahora exige token
def get_categorias(current_user):
    tipo = request.args.get('tipo')
    return listar_categorias_logic(tipo, current_user)

@categoria_bp.route('/categorias', methods=['POST'])
@token_required # <-- Endpoint para crear
def post_categoria(current_user):
    data = request.get_json()
    return crear_categoria_logic(data, current_user)