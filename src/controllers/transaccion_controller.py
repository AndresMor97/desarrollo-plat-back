from src.models.transaccion_model import Transaccion, db
from src.dtos.transaccion_dto import TransaccionDTO
from src.utils.response_helper import standard_response
from marshmallow import ValidationError

transaccion_dto = TransaccionDTO()

def crear_transaccion_logic(data):
    try:
        # 1. Validar datos con el DTO
        validated_data = transaccion_dto.load(data)
        
        # 2. Crear instancia del modelo
        nueva_t = Transaccion(
            id_usuario=validated_data['id_usuario'],
            monto=validated_data['monto'],
            descripcion=validated_data['descripcion'],
            tipo=validated_data['tipo'],
            id_categoria=validated_data.get('id_categoria')
        )
        
        db.session.add(nueva_t)
        db.session.commit()
        
        return standard_response("Registro exitoso", {"id": nueva_t.id_transaccion}, 201)
    
    except ValidationError as err:
        return standard_response("Error de validación", err.messages, 400)
    except Exception as e:
        db.session.rollback()
        return standard_response("Error interno del servidor", str(e), 500)