from src.models.categoria_model import Categoria
from src.dtos.categoria_dto import CategoriaDTO
from src.utils.response_helper import standard_response

# Usamos many=True porque vamos a devolver una lista de categorías
categoria_schema = CategoriaDTO(many=True)

def listar_categorias_logic(tipo=None):
    try:
        # Iniciamos la consulta base
        query = Categoria.query
        
        # Si el cliente envía un filtro (ej. ?tipo=gasto), lo aplicamos en la BD
        if tipo:
            query = query.filter_by(tipo=tipo)
        
        # Ejecutamos la consulta
        categorias = query.all()
        
        # Convertimos los objetos de la base de datos a formato JSON limpio
        resultado = categoria_schema.dump(categorias)
        
        return standard_response("Categorías obtenidas con éxito", resultado, 200)
    
    except Exception as e:
        return standard_response("Error al listar categorías", str(e), 500)