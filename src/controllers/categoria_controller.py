from sqlalchemy import or_, func
from marshmallow import ValidationError
from src.models.categoria_model import Categoria
from src.models.transaccion_model import db, Transaccion  # Agregamos Transaccion para el JOIN
from src.dtos.categoria_dto import CategoriaDTO, SaldoCategoriaDTO # Agregamos el nuevo DTO
from src.utils.response_helper import standard_response

# Instancias de los DTOs
categoria_schema = CategoriaDTO(many=True)
categoria_single_schema = CategoriaDTO() 
saldo_categoria_schema = SaldoCategoriaDTO(many=True) # Instancia para la lista de saldos

def listar_categorias_logic(tipo, current_user):
    """Devuelve las categorías del sistema y las personalizadas del usuario."""
    try:
        # Filtro mágico: Trae las que no tienen dueño (NULL) O las que le pertenecen al usuario del token
        query = Categoria.query.filter(
            or_(Categoria.id_usuario == None, Categoria.id_usuario == current_user.id_usuario)
        )

        # Si además se pide filtrar por "ingreso" o "gasto", lo aplicamos a los resultados anteriores
        if tipo:
            query = query.filter(Categoria.tipo == tipo)

        categorias = query.all()
        resultado = categoria_schema.dump(categorias)

        return standard_response("Categorías obtenidas con éxito", resultado, 200)

    except Exception as e:
        return standard_response("Error al listar categorías", str(e), 500)


def crear_categoria_logic(data, current_user):
    """Permite al usuario crear una categoría personalizada."""
    try:
        # 1. Validar los datos recibidos (nombre y tipo)
        validated_data = categoria_single_schema.load(data)
        
        # 2. Evitar duplicados: Verificar si el usuario ya creó una categoría con ese mismo nombre y tipo
        existe = Categoria.query.filter_by(
            nombre=validated_data['nombre'], 
            id_usuario=current_user.id_usuario,
            tipo=validated_data['tipo']
        ).first()

        if existe:
            return standard_response("Ya tienes una categoría con ese nombre para este tipo", None, 400)

        # 3. Crear la nueva categoría asociándola al usuario actual
        nueva_categoria = Categoria(
            id_usuario=current_user.id_usuario,
            nombre=validated_data['nombre'],
            tipo=validated_data['tipo']
        )
        
        db.session.add(nueva_categoria)
        db.session.commit()
        
        return standard_response("Categoría personalizada creada", {"id": nueva_categoria.id_categoria}, 201)
    
    except ValidationError as err:
        return standard_response("Error de validación", err.messages, 400)
    except Exception as e:
        db.session.rollback()
        return standard_response("Error interno del servidor", str(e), 500)


def eliminar_categoria_logic(id_categoria, current_user):
    """Permite al usuario eliminar una de sus categorías personalizadas."""
    try:
        # Buscamos la categoría por su ID
        categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()

        # 1. Verificamos si existe
        if not categoria:
            return standard_response("Categoría no encontrada", None, 404)

        # 2. Seguridad: Verificamos si es una categoría del sistema
        if categoria.id_usuario is None:
            return standard_response("No puedes eliminar las categorías por defecto del sistema", None, 403)

        # 3. Seguridad: Verificamos si la categoría le pertenece al usuario actual
        if categoria.id_usuario != current_user.id_usuario:
            return standard_response("No tienes permiso para eliminar esta categoría", None, 403)

        # Si pasa las validaciones de seguridad, la eliminamos
        db.session.delete(categoria)
        db.session.commit()

        return standard_response("Categoría eliminada con éxito", None, 200)

    except Exception as e:
        db.session.rollback()
        return standard_response("Error al eliminar la categoría", str(e), 500)


def obtener_saldos_por_categoria_logic(current_user):
    """Calcula cuánto se ha gastado o ingresado en cada categoría del usuario."""
    try:
        # Realizamos un JOIN entre Categorias y Transacciones
        # Sumamos el monto agrupando por el ID de la categoría
        resultados = db.session.query(
            Categoria.id_categoria,
            Categoria.nombre,
            Categoria.tipo,
            func.sum(Transaccion.monto).label('total_acumulado')
        ).join(
            Transaccion, Categoria.id_categoria == Transaccion.id_categoria
        ).filter(
            Transaccion.id_usuario == current_user.id_usuario
        ).group_by(
            Categoria.id_categoria
        ).all()

        # Convertimos los resultados de la consulta en una lista de diccionarios
        data = []
        for r in resultados:
            data.append({
                "id_categoria": r.id_categoria,
                "nombre": r.nombre,
                "tipo": r.tipo,
                "total_acumulado": float(r.total_acumulado)
            })

        # Validamos y volcamos la data con nuestro DTO
        resultado = saldo_categoria_schema.dump(data)

        return standard_response("Saldos por categoría obtenidos", resultado, 200)

    except Exception as e:
        return standard_response("Error al calcular saldos por categoría", str(e), 500)