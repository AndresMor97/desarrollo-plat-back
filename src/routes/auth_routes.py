from flask import Blueprint, request
from src.controllers.auth_controller import registrar_usuario_logic, login_usuario_logic

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/registro', methods=['POST'])
def registro():
    return registrar_usuario_logic(request.get_json())

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_usuario_logic(request.get_json())