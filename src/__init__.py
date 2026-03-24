from flask import Flask
from flask_cors import CORS
from src.models.transaccion_model import db
from src.dtos.transaccion_dto import ma
from src.routes.transaccion_routes import transaccion_bp
from src.utils.response_helper import standard_response
from src.routes.usuario_routes import usuario_bp

def create_app():
    # 1. Crear la instancia de Flask
    app = Flask(__name__)

    # 2. Cargar la configuración (Asegúrate de tener el archivo config.py en la raíz)
    app.config.from_object('config.Config')

    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 3. Inicializar extensiones
    # Vincular SQLAlchemy y Marshmallow a la aplicación
    db.init_app(app)
    ma.init_app(app)

    # 4. Manejo global de errores (Para rutas que no existen)
    @app.errorhandler(404)
    def not_found(e):
        return standard_response("El recurso solicitado no existe", None, 404)

    @app.errorhandler(500)
    def server_error(e):
        return standard_response("Error interno del servidor", str(e), 500)

    # 5. Registro de Blueprints
    # Esto une las rutas de transacciones con el prefijo /api
    app.register_blueprint(transaccion_bp, url_prefix='/api')
    app.register_blueprint(usuario_bp, url_prefix='/api')

    return app