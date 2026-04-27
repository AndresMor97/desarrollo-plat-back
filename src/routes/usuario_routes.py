from flask import Blueprint
from src.controllers.usuario_controller import listar_usuarios_logic
from src.utils.auth_middleware import token_required

usuario_bp = Blueprint('usuario_bp', __name__)


@usuario_bp.route('/usuarios', methods=['GET'])
@token_required
def get_usuarios(current_user):
    """Devuelve la lista de todos los usuarios."""
    return listar_usuarios_logic()
