import jwt
import datetime
from functools import wraps
from flask import request, current_app
from src.utils.response_helper import standard_response
from src.models.usuario_model import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Formato: "Bearer <token>"
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header

        if not token:
            return standard_response("Token faltante", None, 401)

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Usuario.query.get(data['id_usuario'])
            if not current_user:
                raise Exception("Usuario no encontrado")
        except jwt.ExpiredSignatureError:
            return standard_response("El token ha expirado", None, 401)
        except Exception as e:
            return standard_response("Token inválido", str(e), 401)

        return f(current_user, *args, **kwargs)

    return decorated

def generate_token(usuario_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        'iat': datetime.datetime.utcnow(),
        'id_usuario': usuario_id
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")