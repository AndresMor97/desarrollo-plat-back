from src.models.usuario_model import Usuario # Asumiendo que ya tienes el modelo
from src.dtos.usuario_dto import UsuarioDTO
from src.utils.response_helper import standard_response

usuario_schema = UsuarioDTO(many=True)

def listar_usuarios_logic():
    try:
        # Consultar todos los usuarios en la DB
        usuarios = Usuario.query.all()
        
        # Transformar los modelos en datos limpios (JSON-ready)
        resultado = usuario_schema.dump(usuarios)
        
        return standard_response("Lista de usuarios obtenida", resultado, 200)
    
    except Exception as e:
        return standard_response("Error al obtener usuarios", str(e), 500)