from src.models.usuario_model import Usuario
from src.dtos.usuario_dto import UsuarioDTO
from src.utils.response_helper import standard_response

usuario_schema = UsuarioDTO(many=True)


def listar_usuarios_logic():
    """Devuelve una lista de todos los usuarios registrados."""
    try:
        usuarios = Usuario.query.all()
        resultado = usuario_schema.dump(usuarios)
        return standard_response("Lista de usuarios obtenida", resultado, 200)

    except Exception as e:
        return standard_response("Error al obtener usuarios", str(e), 500)
