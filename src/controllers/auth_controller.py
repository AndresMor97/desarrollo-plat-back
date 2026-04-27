from werkzeug.security import generate_password_hash, check_password_hash
from src.models.usuario_model import Usuario, db
from src.utils.auth_middleware import generate_token
from src.utils.response_helper import standard_response

def registrar_usuario_logic(data):
    try:
        if Usuario.query.filter_by(email=data['email']).first():
            return standard_response("El correo ya está registrado", None, 400)

        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return standard_response("Usuario registrado con éxito", {"id": nuevo_usuario.id_usuario}, 201)
    except Exception as e:
        return standard_response("Error al registrar", str(e), 500)

def login_usuario_logic(data):
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if usuario and check_password_hash(usuario.password_hash, data['password']):
        token = generate_token(usuario.id_usuario)
        return standard_response("Login exitoso", {"token": token, "nombre": usuario.nombre}, 200)
    
    return standard_response("Credenciales incorrectas", None, 401)