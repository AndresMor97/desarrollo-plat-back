from flask import Blueprint
from src.controllers.usuario_controller import listar_usuarios_logic

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    return listar_usuarios_logic()