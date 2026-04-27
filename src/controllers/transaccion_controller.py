from sqlalchemy import func
from marshmallow import ValidationError
from src.models.transaccion_model import Transaccion, db
from src.models.categoria_model import Categoria
from src.dtos.transaccion_dto import TransaccionDTO
from src.dtos.saldo_dto import SaldoDTO
from src.utils.response_helper import standard_response

transaccion_dto = TransaccionDTO()
transacciones_list_dto = TransaccionDTO(many=True)
saldo_schema = SaldoDTO()


def crear_transaccion_logic(data, current_user):
    """Registra una nueva transacción para el usuario autenticado."""
    try:
        validated_data = transaccion_dto.load(data)

        nueva_t = Transaccion(
            id_usuario=current_user.id_usuario,
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


def obtener_saldo_logic(current_user):
    """Calcula el saldo total (ingresos menos gastos) del usuario."""
    try:
        ingresos = db.session.query(func.sum(Transaccion.monto)).filter(
            Transaccion.id_usuario == current_user.id_usuario,
            Transaccion.tipo == 'ingreso'
        ).scalar() or 0

        gastos = db.session.query(func.sum(Transaccion.monto)).filter(
            Transaccion.id_usuario == current_user.id_usuario,
            Transaccion.tipo == 'gasto'
        ).scalar() or 0

        saldo_total = float(ingresos) - float(gastos)

        resultado = {
            "id_usuario": current_user.id_usuario,
            "total_ingresos": float(ingresos),
            "total_gastos": float(gastos),
            "saldo_actual": saldo_total
        }

        return standard_response("Saldo calculado", saldo_schema.dump(resultado), 200)

    except Exception as e:
        return standard_response("Error en el cálculo", str(e), 500)


def listar_historial_logic(current_user):
    """Devuelve el historial de transacciones ordenadas por fecha."""
    try:
        query = db.session.query(
            Transaccion.id_transaccion,
            Transaccion.monto,
            Transaccion.descripcion,
            Transaccion.tipo,
            Transaccion.fecha_transaccion,
            Categoria.nombre.label('categoria_nombre')
        ).join(
            Categoria, Transaccion.id_categoria == Categoria.id_categoria, isouter=True
        ).filter(
            Transaccion.id_usuario == current_user.id_usuario
        ).order_by(
            Transaccion.fecha_transaccion.desc()
        ).all()

        historial = []
        for t in query:
            historial.append({
                "id": t.id_transaccion,
                "monto": float(t.monto),
                "descripcion": t.descripcion,
                "tipo": t.tipo,
                "fecha": t.fecha_transaccion.strftime('%Y-%m-%d'),
                "categoria": t.categoria_nombre or "Sin categoría"
            })

        return standard_response("Historial obtenido con éxito", historial, 200)

    except Exception as e:
        return standard_response("Error al obtener el historial", str(e), 500)


def obtener_estadisticas_gastos_logic(current_user):
    """Devuelve los gastos totales agrupados por categoría."""
    try:
        estadisticas = db.session.query(
            Categoria.nombre.label('categoria_nombre'),
            func.sum(Transaccion.monto).label('total')
        ).join(
            Categoria, Transaccion.id_categoria == Categoria.id_categoria, isouter=True
        ).filter(
            Transaccion.id_usuario == current_user.id_usuario,
            Transaccion.tipo == 'gasto'
        ).group_by(
            Categoria.nombre
        ).all()

        resultado = []
        for est in estadisticas:
            resultado.append({
                "categoria": est.categoria_nombre or "Otros",
                "total": float(est.total)
            })

        return standard_response("Estadísticas obtenidas", resultado, 200)

    except Exception as e:
        return standard_response("Error al obtener estadísticas", str(e), 500)


def eliminar_transaccion_logic(id_transaccion, current_user):
    """Elimina una transacción verificando que pertenezca al usuario."""
    try:
        transaccion = Transaccion.query.filter_by(
            id_transaccion=id_transaccion,
            id_usuario=current_user.id_usuario
        ).first()

        if not transaccion:
            return standard_response("Transacción no encontrada o no autorizada", None, 404)

        db.session.delete(transaccion)
        db.session.commit()

        return standard_response("Transacción eliminada con éxito", None, 200)

    except Exception as e:
        db.session.rollback()
        return standard_response("Error al eliminar la transacción", str(e), 500)
