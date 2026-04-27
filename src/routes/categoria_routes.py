from flask import Blueprint, request
from src.controllers.categoria_controller import listar_categorias_logic

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categorias', methods=['GET'])
def get_categorias():
    # Permite filtrar como: /api/categorias?tipo=gasto
    tipo = request.args.get('tipo')
    return listar_categorias_logic(tipo)