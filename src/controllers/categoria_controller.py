from sqlalchemy import or_, func, case
from marshmallow import ValidationError
from src.models.categoria_model import Categoria
from src.models.transaccion_model import db, Transaccion
from src.dtos.categoria_dto import CategoriaDTO, SaldoCategoriaDTO
from src.utils.response_helper import standard_response

# Instancias de los DTOs
categoria_schema = CategoriaDTO(many=True)
categoria_single_schema = CategoriaDTO() 
saldo_categoria_schema = SaldoCategoriaDTO(many=True)

def listar_categorias_logic(current_user):
    """Devuelve todas las categorías (generales)."""
    try:
        query = Categoria.query.filter(
            or_(Categoria.id_usuario == None, Categoria.id_usuario == current_user.id_usuario)
        )

        categorias = query.all()
        resultado = categoria_schema.dump(categorias)

        return standard_response("Categorías obtenidas con éxito", resultado, 200)

    except Exception as e:
        return standard_response("Error al listar categorías", str(e), 500)


def crear_categoria_logic(data, current_user):
    """Permite al usuario crear una categoría personalizada general."""
    try:
        validated_data = categoria_single_schema.load(data)
        
        existe = Categoria.query.filter_by(
            nombre=validated_data['nombre'], 
            id_usuario=current_user.id_usuario
        ).first()

        if existe:
            return standard_response("Ya tienes una categoría con ese nombre", None, 400)

        nueva_categoria = Categoria(
            id_usuario=current_user.id_usuario,
            nombre=validated_data['nombre']
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
        categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()

        if not categoria:
            return standard_response("Categoría no encontrada", None, 404)

        if categoria.id_usuario is None:
            return standard_response("No puedes eliminar las categorías por defecto del sistema", None, 403)

        if categoria.id_usuario != current_user.id_usuario:
            return standard_response("No tienes permiso para eliminar esta categoría", None, 403)

        db.session.delete(categoria)
        db.session.commit()

        return standard_response("Categoría eliminada con éxito", None, 200)

    except Exception as e:
        db.session.rollback()
        return standard_response("Error al eliminar la categoría", str(e), 500)


def obtener_saldos_por_categoria_logic(current_user):
    """Calcula el total de ingresos, gastos y el saldo neto por categoría."""
    try:
        # Sumamos solo si es ingreso; si no, suma 0
        sum_ingresos = func.sum(case((Transaccion.tipo == 'ingreso', Transaccion.monto), else_=0))
        # Sumamos solo si es gasto; si no, suma 0
        sum_gastos = func.sum(case((Transaccion.tipo == 'gasto', Transaccion.monto), else_=0))

        resultados = db.session.query(
            Categoria.id_categoria,
            Categoria.nombre,
            sum_ingresos.label('total_ingresos'),
            sum_gastos.label('total_gastos')
        ).join(
            Transaccion, Categoria.id_categoria == Transaccion.id_categoria
        ).filter(
            Transaccion.id_usuario == current_user.id_usuario
        ).group_by(
            Categoria.id_categoria
        ).all()

        data = []
        for r in resultados:
            ingresos = float(r.total_ingresos or 0)
            gastos = float(r.total_gastos or 0)
            data.append({
                "id_categoria": r.id_categoria,
                "nombre": r.nombre,
                "total_ingresos": ingresos,
                "total_gastos": gastos,
                "saldo_total": ingresos - gastos  # <-- Aquí hacemos la matemática final
            })

        resultado = saldo_categoria_schema.dump(data)

        return standard_response("Saldos por categoría obtenidos", resultado, 200)

    except Exception as e:
        return standard_response("Error al calcular saldos por categoría", str(e), 500)