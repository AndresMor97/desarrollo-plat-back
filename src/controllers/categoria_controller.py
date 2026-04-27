from src.models.categoria_model import Categoria
from src.dtos.categoria_dto import CategoriaDTO
from src.utils.response_helper import standard_response

categoria_schema = CategoriaDTO(many=True)


def listar_categorias_logic(tipo=None):
    """Devuelve una lista de categorías, opcionalmente filtradas por tipo."""
    try:
        query = Categoria.query

        if tipo:
            query = query.filter_by(tipo=tipo)

        categorias = query.all()
        resultado = categoria_schema.dump(categorias)

        return standard_response("Categorías obtenidas con éxito", resultado, 200)

    except Exception as e:
        return standard_response("Error al listar categorías", str(e), 500)
