from flask import Blueprint
from src.controllers.usuario_controller import listar_usuarios_logic
from src.utils.auth_middleware import token_required

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
@token_required
def get_usuarios(current_user):
    # Aunque listar_usuarios_logic no use current_user, 
    # la ruta exige que exista un token válido para responder.
    return listar_usuarios_logic()